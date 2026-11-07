using Apexive.CoreRpa.Contracts;
using System.Text;
using System.Text.Json;

namespace Apexive.CoreRpa.Windows.Agent;

public sealed class AgentWorker(
    OrchestratorClient orchestrator,
    RuntimeEngine runtimeEngine,
    AgentOptions options,
    ILogger<AgentWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await orchestrator.EnsureBotReadyAsync(stoppingToken);
        await RunPollLoopAsync(stoppingToken);
    }

    private async Task RunPollLoopAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var job = await orchestrator.ClaimAsync(stoppingToken);
                if (job is null)
                {
                    await orchestrator.HeartbeatAsync(stoppingToken);
                    await Task.Delay(TimeSpan.FromSeconds(options.PollIntervalSeconds), stoppingToken);
                    continue;
                }

                await ExecuteJobAsync(job, stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                break;
            }
            catch (HttpRequestException exception)
            {
                logger.LogError(exception, "CoreRPA orchestrator request failed.");
                await Task.Delay(TimeSpan.FromSeconds(options.PollIntervalSeconds), stoppingToken);
            }
            catch (System.Text.Json.JsonException exception)
            {
                logger.LogError(exception, "CoreRPA orchestrator returned an invalid response.");
                await Task.Delay(TimeSpan.FromSeconds(options.PollIntervalSeconds), stoppingToken);
            }
        }
    }

    private async Task ExecuteJobAsync(RuntimeJob job, CancellationToken stoppingToken)
    {
        using var heartbeatCancellation = CancellationTokenSource.CreateLinkedTokenSource(stoppingToken);
        var heartbeatTask = RunHeartbeatAsync(heartbeatCancellation.Token);
        RuntimeCompletion completion;
        try
        {
            completion = await runtimeEngine.ExecuteAsync(job, stoppingToken);
        }
        catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
        {
            throw;
        }
        catch (RuntimeContractException exception)
        {
            logger.LogError(
                exception,
                "Execution {ExecutionId} failed runtime validation.",
                job.ExecutionId);
            completion = new RuntimeCompletion("FAILED", null, exception.Message);
        }
        catch (InvalidOperationException exception)
        {
            logger.LogError(
                exception,
                "Execution {ExecutionId} could not be completed.",
                job.ExecutionId);
            completion = new RuntimeCompletion("FAILED", null, exception.Message);
        }
        catch (HttpRequestException exception)
        {
            logger.LogError(exception, "AIS model request for execution {ExecutionId} failed.", job.ExecutionId);
            completion = new RuntimeCompletion("FAILED", null, exception.Message);
        }
        catch (System.Text.Json.JsonException exception)
        {
            logger.LogError(exception, "Execution {ExecutionId} received an invalid model response.", job.ExecutionId);
            completion = new RuntimeCompletion("FAILED", null, exception.Message);
        }
        catch (OperationCanceledException exception) when (!stoppingToken.IsCancellationRequested)
        {
            logger.LogError(exception, "Execution {ExecutionId} exceeded a runtime request timeout.", job.ExecutionId);
            completion = new RuntimeCompletion("FAILED", null, "The runtime request timed out.");
        }

        if (completion.ResultData is JsonElement resultData
            && Encoding.UTF8.GetByteCount(resultData.GetRawText()) > 1_000_000)
        {
            completion = new RuntimeCompletion(
                "FAILED",
                null,
                "Runtime result_data exceeded the 1 MB orchestrator limit.");
        }

        try
        {
            await CompleteWithRetryAsync(job, completion, stoppingToken);
            logger.LogInformation(
                "Execution {ExecutionId} completed with status {Status}.",
                job.ExecutionId,
                completion.Status);
        }
        finally
        {
            heartbeatCancellation.Cancel();
            try
            {
                await heartbeatTask;
            }
            catch (OperationCanceledException) when (heartbeatCancellation.IsCancellationRequested)
            {
            }
        }
    }

    private async Task CompleteWithRetryAsync(
        RuntimeJob job,
        RuntimeCompletion completion,
        CancellationToken stoppingToken)
    {
        var delay = TimeSpan.FromSeconds(1);
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await orchestrator.CompleteAsync(job, completion, stoppingToken);
                return;
            }
            catch (HttpRequestException exception)
                when (exception.StatusCode is null || (int)exception.StatusCode >= 500)
            {
                logger.LogError(
                    exception,
                    "Completion delivery for execution {ExecutionId} failed; retrying.",
                    job.ExecutionId);
                await Task.Delay(delay, stoppingToken);
                delay = TimeSpan.FromSeconds(Math.Min(delay.TotalSeconds * 2, 30));
            }
        }
    }

    private async Task RunHeartbeatAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await orchestrator.HeartbeatAsync(stoppingToken);
                await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                break;
            }
            catch (HttpRequestException exception)
            {
                logger.LogError(exception, "CoreRPA agent heartbeat failed.");
                await Task.Delay(TimeSpan.FromSeconds(options.PollIntervalSeconds), stoppingToken);
            }
        }
    }
}

using System.Net;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using Apexive.CoreRpa.Contracts;

namespace Apexive.CoreRpa.Windows.Agent;

public sealed class OrchestratorClient(HttpClient httpClient, AgentOptions options)
{
    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web);
    private readonly SemaphoreSlim _tokenLock = new(1, 1);
    private string? _accessToken;
    private DateTimeOffset _tokenExpiresAt;

    public async Task EnsureBotReadyAsync(CancellationToken cancellationToken)
    {
        using var request = await CreateApiRequestAsync(
            HttpMethod.Get,
            "/api/v1/automation/bots?limit=200",
            cancellationToken);
        using var response = await httpClient.SendAsync(request, cancellationToken);
        await EnsureSuccessAsync(response, cancellationToken);
        using var payload = JsonDocument.Parse(await response.Content.ReadAsStreamAsync(cancellationToken));
        if (!payload.RootElement.TryGetProperty("items", out var items)
            || items.ValueKind != JsonValueKind.Array)
        {
            throw new JsonException("The automation bot list response is malformed.");
        }

        var bot = items.EnumerateArray().FirstOrDefault(candidate =>
            candidate.TryGetProperty("id", out var id)
            && Guid.TryParse(id.GetString(), out var parsedId)
            && parsedId == options.BotId);
        if (bot.ValueKind == JsonValueKind.Undefined)
        {
            throw new InvalidOperationException("The configured bot is not registered in this tenant.");
        }

        var state = bot.GetProperty("status").GetString();
        if (state == "OFFLINE")
        {
            await SendApiAsync(
                HttpMethod.Post,
                $"/api/v1/automation/bots/{options.BotId}/control",
                new { action = "START" },
                cancellationToken);
        }
        else if (state is not ("IDLE" or "BUSY"))
        {
            throw new InvalidOperationException($"The configured bot cannot start from state {state}.");
        }
    }

    public async Task HeartbeatAsync(CancellationToken cancellationToken)
    {
        await SendApiAsync(
            HttpMethod.Post,
            $"/api/v1/automation/bots/{options.BotId}/heartbeat",
            null,
            cancellationToken);
    }

    public async Task<RuntimeJob?> ClaimAsync(CancellationToken cancellationToken)
    {
        using var request = await CreateApiRequestAsync(
            HttpMethod.Post,
            $"/api/v1/automation/bots/{options.BotId}/claim",
            cancellationToken);
        using var response = await httpClient.SendAsync(request, cancellationToken);
        await EnsureSuccessAsync(response, cancellationToken);
        if (response.StatusCode == HttpStatusCode.NoContent)
        {
            return null;
        }

        using var payload = await JsonDocument.ParseAsync(
            await response.Content.ReadAsStreamAsync(cancellationToken),
            cancellationToken: cancellationToken);
        if (payload.RootElement.ValueKind == JsonValueKind.Null)
        {
            return null;
        }

        var root = payload.RootElement;
        if (!root.TryGetProperty("definition", out var definition)
            || !root.TryGetProperty("input_data", out var inputData))
        {
            throw new JsonException("The runtime claim response is malformed.");
        }

        return new RuntimeJob(
            root.GetProperty("execution_id").GetGuid(),
            root.GetProperty("tenant_id").GetGuid(),
            root.GetProperty("workflow_id").GetGuid(),
            root.GetProperty("workflow_version").GetInt32(),
            root.GetProperty("claim_attempt").GetInt32(),
            root.GetProperty("contract_version").GetInt32(),
            root.GetProperty("runtime").GetString()
                ?? throw new JsonException("The claimed runtime is missing."),
            definition.Clone(),
            inputData.Clone());
    }

    public async Task CompleteAsync(
        RuntimeJob job,
        RuntimeCompletion completion,
        CancellationToken cancellationToken)
    {
        var body = new
        {
            status = completion.Status,
            claim_attempt = job.ClaimAttempt,
            result_data = completion.ResultData,
            error_message = completion.ErrorMessage,
        };
        await SendApiAsync(
            HttpMethod.Post,
            $"/api/v1/automation/bots/{options.BotId}/executions/{job.ExecutionId}/complete",
            body,
            cancellationToken);
    }

    private async Task SendApiAsync(
        HttpMethod method,
        string path,
        object? body,
        CancellationToken cancellationToken)
    {
        using var request = await CreateApiRequestAsync(method, path, cancellationToken);
        if (body is not null)
        {
            request.Content = new StringContent(
                JsonSerializer.Serialize(body, JsonOptions),
                Encoding.UTF8,
                "application/json");
        }

        using var response = await httpClient.SendAsync(request, cancellationToken);
        await EnsureSuccessAsync(response, cancellationToken);
    }

    private async Task<HttpRequestMessage> CreateApiRequestAsync(
        HttpMethod method,
        string path,
        CancellationToken cancellationToken)
    {
        var request = new HttpRequestMessage(
            method,
            new Uri(new Uri(options.ApiBaseUrl.TrimEnd('/') + "/"), path.TrimStart('/')));
        request.Headers.Authorization =
            new AuthenticationHeaderValue("Bearer", await GetAccessTokenAsync(cancellationToken));
        return request;
    }

    private async Task<string> GetAccessTokenAsync(CancellationToken cancellationToken)
    {
        if (_accessToken is not null && _tokenExpiresAt > DateTimeOffset.UtcNow.AddSeconds(30))
        {
            return _accessToken;
        }

        await _tokenLock.WaitAsync(cancellationToken);
        try
        {
            if (_accessToken is not null && _tokenExpiresAt > DateTimeOffset.UtcNow.AddSeconds(30))
            {
                return _accessToken;
            }

            using var request = new HttpRequestMessage(HttpMethod.Post, options.TokenUrl)
            {
                Content = new FormUrlEncodedContent(new Dictionary<string, string>
                {
                    ["grant_type"] = "client_credentials",
                    ["client_id"] = options.ClientId,
                    ["client_secret"] = options.ClientSecret,
                }),
            };
            using var response = await httpClient.SendAsync(request, cancellationToken);
            await EnsureSuccessAsync(response, cancellationToken);
            using var payload = await JsonDocument.ParseAsync(
                await response.Content.ReadAsStreamAsync(cancellationToken),
                cancellationToken: cancellationToken);
            _accessToken = payload.RootElement.GetProperty("access_token").GetString()
                ?? throw new JsonException("The identity provider returned an empty access token.");
            var expiresIn = payload.RootElement.TryGetProperty("expires_in", out var expiry)
                ? expiry.GetInt32()
                : 300;
            _tokenExpiresAt = DateTimeOffset.UtcNow.AddSeconds(Math.Max(60, expiresIn));
            return _accessToken;
        }
        finally
        {
            _tokenLock.Release();
        }
    }

    private static async Task EnsureSuccessAsync(
        HttpResponseMessage response,
        CancellationToken cancellationToken)
    {
        if (response.IsSuccessStatusCode)
        {
            return;
        }

        throw new HttpRequestException(
            $"Orchestrator request failed with {(int)response.StatusCode}.",
            null,
            response.StatusCode);
    }
}

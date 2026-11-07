using System.Text.Json;
using Apexive.CoreRpa.Ais.Runtime;
using Apexive.CoreRpa.Contracts;
using Apexive.CoreRpa.Cy.Runtime;
using Xunit;

namespace Apexive.CoreRpa.Runtime.Tests;

public sealed class RuntimeTests
{
    [Fact]
    public async Task AisRuntimeEvaluatesOnlyAllowlistedVariableAndModelSteps()
    {
        var job = CreateJob(
            RuntimeNames.Ais,
            """{"runtime":"AIS","contract_version":1,"steps":[{"type":"set_variable","key":"status","value":"ready"}]}""",
            """{"input":"data"}""");

        var result = await new AisWorkflowRuntime().ExecuteAsync(job);
        Assert.Equal("SUCCEEDED", result.Status);
        Assert.Equal("ready", result.ResultData!.Value.GetProperty("variables").GetProperty("status").GetString());
    }

    [Fact]
    public async Task AisRuntimeRequiresExplicitModelProviderForPromptSteps()
    {
        var job = CreateJob(
            RuntimeNames.Ais,
            """{"runtime":"AIS","contract_version":1,"steps":[{"type":"prompt","key":"answer","prompt":"classify"}]}""",
            "{}");

        var exception = await Assert.ThrowsAsync<RuntimeContractException>(
            async () => await new AisWorkflowRuntime().ExecuteAsync(job));
        Assert.Contains("configured text model provider", exception.Message);
    }

    [Fact]
    public async Task AisRuntimeSubstitutesInputIntoConfiguredModelPrompt()
    {
        var provider = new RecordingModelProvider();
        var job = CreateJob(
            RuntimeNames.Ais,
            """{"runtime":"AIS","contract_version":1,"steps":[{"type":"prompt","key":"answer","prompt":"Classify: {{text}}"}]}""",
            """{"text":"local input"}""");

        var result = await new AisWorkflowRuntime(provider).ExecuteAsync(job);
        Assert.Equal("Classify: local input", provider.Prompt);
        Assert.Equal("complete", result.ResultData!.Value.GetProperty("variables").GetProperty("answer").GetString());
    }

    [Fact]
    public async Task CyRuntimeEmitsAlertsAndHumanReviewProposalsWithoutExecutingActions()
    {
        var job = CreateJob(
            RuntimeNames.Cy,
            """{"runtime":"CY","contract_version":1,"rules":[{"id":"failed-login","field":"event.type","equals":"failed_login","severity":"HIGH","title":"Repeated login failure","recommended_response":"Review the account activity"}]}""",
            """{"events":[{"event":{"type":"failed_login"}}]}""");

        var result = await new CyWorkflowRuntime().ExecuteAsync(job);
        var resultData = result.ResultData!.Value;
        Assert.Equal(1, resultData.GetProperty("alerts").GetArrayLength());
        Assert.True(resultData.GetProperty("requires_human_review").GetBoolean());
    }

    [Fact]
    public async Task RuntimeEngineRejectsUnknownContractVersions()
    {
        using var definition = JsonDocument.Parse("""{"runtime":"CY","contract_version":1,"rules":[]}""");
        using var input = JsonDocument.Parse("{}");
        var job = new RuntimeJob(
            Guid.NewGuid(), Guid.NewGuid(), Guid.NewGuid(), 1, 1, 2, RuntimeNames.Cy,
            definition.RootElement, input.RootElement);

        var engine = new RuntimeEngine([new CyWorkflowRuntime()]);
        var exception = Assert.Throws<RuntimeContractException>(() => engine.ExecuteAsync(job));
        Assert.Contains("Unsupported runtime contract version", exception.Message);
    }

    private static RuntimeJob CreateJob(string runtime, string definition, string input)
    {
        using var definitionDocument = JsonDocument.Parse(definition);
        using var inputDocument = JsonDocument.Parse(input);
        return new RuntimeJob(
            Guid.NewGuid(),
            Guid.NewGuid(),
            Guid.NewGuid(),
            1,
            1,
            RuntimeNames.ContractVersion,
            runtime,
            definitionDocument.RootElement.Clone(),
            inputDocument.RootElement.Clone());
    }

    private sealed class RecordingModelProvider : ITextModelProvider
    {
        public string? Prompt { get; private set; }

        public ValueTask<string> CompleteAsync(
            string prompt,
            CancellationToken cancellationToken = default)
        {
            Prompt = prompt;
            return ValueTask.FromResult("complete");
        }
    }
}

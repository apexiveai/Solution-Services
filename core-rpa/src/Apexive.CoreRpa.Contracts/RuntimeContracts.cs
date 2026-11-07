using System.Text.Json;

namespace Apexive.CoreRpa.Contracts;

public static class RuntimeNames
{
    public const string Ais = "AIS";
    public const string Cy = "CY";
    public const int ContractVersion = 1;
}

public sealed record RuntimeJob(
    Guid ExecutionId,
    Guid TenantId,
    Guid WorkflowId,
    int WorkflowVersion,
    int ClaimAttempt,
    int ContractVersion,
    string Runtime,
    JsonElement Definition,
    JsonElement InputData);

public sealed record RuntimeCompletion(
    string Status,
    JsonElement? ResultData,
    string? ErrorMessage);

public interface IRuntimeEngine
{
    string Runtime { get; }
    ValueTask<RuntimeCompletion> ExecuteAsync(
        RuntimeJob job,
        CancellationToken cancellationToken = default);
}

public interface ITextModelProvider
{
    ValueTask<string> CompleteAsync(
        string prompt,
        CancellationToken cancellationToken = default);
}

public sealed class RuntimeContractException(string message) : Exception(message);

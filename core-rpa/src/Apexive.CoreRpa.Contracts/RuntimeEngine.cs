using System.Text.Json;

namespace Apexive.CoreRpa.Contracts;

public sealed class RuntimeEngine(IEnumerable<IRuntimeEngine> engines)
{
    private readonly IReadOnlyDictionary<string, IRuntimeEngine> _engines =
        engines.ToDictionary(engine => engine.Runtime, StringComparer.OrdinalIgnoreCase);

    public ValueTask<RuntimeCompletion> ExecuteAsync(
        RuntimeJob job,
        CancellationToken cancellationToken = default)
    {
        if (job.ContractVersion != RuntimeNames.ContractVersion)
        {
            throw new RuntimeContractException(
                $"Unsupported runtime contract version {job.ContractVersion}.");
        }

        if (!_engines.TryGetValue(job.Runtime, out var engine))
        {
            throw new RuntimeContractException($"Runtime '{job.Runtime}' is not installed.");
        }

        if (job.Definition.ValueKind != JsonValueKind.Object
            || !job.InputData.ValueKind.Equals(JsonValueKind.Object))
        {
            throw new RuntimeContractException("Runtime definition and input must be JSON objects.");
        }

        return engine.ExecuteAsync(job, cancellationToken);
    }
}

using System.Text.Json;
using System.Text.Json.Nodes;
using System.Text;
using Apexive.CoreRpa.Contracts;

namespace Apexive.CoreRpa.Ais.Runtime;

public sealed class AisWorkflowRuntime(ITextModelProvider? modelProvider = null) : IRuntimeEngine
{
    private const int MaxSteps = 200;
    public string Runtime => RuntimeNames.Ais;

    public async ValueTask<RuntimeCompletion> ExecuteAsync(
        RuntimeJob job,
        CancellationToken cancellationToken = default)
    {
        ValidateJob(job);
        var variables = JsonNode.Parse(job.InputData.GetRawText())!.AsObject();
        var steps = job.Definition.GetProperty("steps").EnumerateArray();
        var count = 0;
        foreach (var step in steps)
        {
            cancellationToken.ThrowIfCancellationRequested();
            if (++count > MaxSteps)
            {
                throw new RuntimeContractException($"AIS workflows may contain at most {MaxSteps} steps.");
            }

            var type = RequiredString(step, "type");
            switch (type)
            {
                case "set_variable":
                    EnsureProperties(step, "type", "key", "value");
                    variables[RequiredString(step, "key")] =
                        JsonNode.Parse(step.GetProperty("value").GetRawText());
                    break;
                case "prompt":
                    EnsureProperties(step, "type", "key", "prompt");
                    if (modelProvider is null)
                    {
                        throw new RuntimeContractException(
                            "AIS prompt execution requires a configured text model provider.");
                    }

                    var promptTemplate = RequiredString(step, "prompt");
                    if (promptTemplate.Length > 8000)
                    {
                        throw new RuntimeContractException("AIS prompts cannot exceed 8000 characters.");
                    }

                    var prompt = ExpandPrompt(promptTemplate, variables);
                    var response = await modelProvider.CompleteAsync(prompt, cancellationToken);
                    variables[RequiredString(step, "key")] = JsonValue.Create(response);
                    break;
                default:
                    throw new RuntimeContractException($"AIS action '{type}' is not supported.");
            }
        }

        var result = JsonSerializer.SerializeToElement(new { variables });
        return new RuntimeCompletion("SUCCEEDED", result, null);
    }

    private static void ValidateJob(RuntimeJob job)
    {
        if (!string.Equals(job.Runtime, RuntimeNames.Ais, StringComparison.OrdinalIgnoreCase))
        {
            throw new RuntimeContractException("AIS runtime received a job for another runtime.");
        }

        var definitionRuntime = RequiredString(job.Definition, "runtime");
        if (!string.Equals(definitionRuntime, RuntimeNames.Ais, StringComparison.OrdinalIgnoreCase)
            || !job.Definition.TryGetProperty("contract_version", out var contractVersion)
            || contractVersion.ValueKind != JsonValueKind.Number
            || contractVersion.GetInt32() != RuntimeNames.ContractVersion
            || !job.Definition.TryGetProperty("steps", out var steps)
            || steps.ValueKind != JsonValueKind.Array)
        {
            throw new RuntimeContractException("AIS workflow definition does not match contract version 1.");
        }

        if (steps.GetArrayLength() > MaxSteps)
        {
            throw new RuntimeContractException($"AIS workflows may contain at most {MaxSteps} steps.");
        }
    }

    private static string RequiredString(JsonElement element, string property)
    {
        if (!element.TryGetProperty(property, out var value)
            || value.ValueKind != JsonValueKind.String
            || string.IsNullOrWhiteSpace(value.GetString()))
        {
            throw new RuntimeContractException($"AIS action requires a non-empty '{property}'.");
        }

        return value.GetString()!;
    }

    private static void EnsureProperties(JsonElement element, params string[] expected)
    {
        var properties = element.EnumerateObject().Select(property => property.Name).ToHashSet(StringComparer.Ordinal);
        if (!properties.SetEquals(expected))
        {
            throw new RuntimeContractException("AIS step contains unsupported fields.");
        }
    }

    private static string ExpandPrompt(string template, JsonObject variables)
    {
        var output = new StringBuilder(template.Length);
        var offset = 0;
        while (offset < template.Length)
        {
            var start = template.IndexOf("{{", offset, StringComparison.Ordinal);
            if (start < 0)
            {
                output.Append(template, offset, template.Length - offset);
                break;
            }

            output.Append(template, offset, start - offset);
            var end = template.IndexOf("}}", start + 2, StringComparison.Ordinal);
            if (end < 0)
            {
                throw new RuntimeContractException("AIS prompt contains an unclosed variable placeholder.");
            }

            var key = template[(start + 2)..end].Trim();
            if (key.Length is 0 or > 64
                || !key.All(character => char.IsAsciiLetterOrDigit(character) || character == '_')
                || !variables.TryGetPropertyValue(key, out var value)
                || value is null)
            {
                throw new RuntimeContractException($"AIS prompt references an unavailable variable '{key}'.");
            }

            output.Append(value is JsonValue jsonValue && jsonValue.TryGetValue<string>(out var text)
                ? text
                : value.ToJsonString());
            offset = end + 2;
        }

        if (output.Length > 16_000)
        {
            throw new RuntimeContractException("Expanded AIS prompt cannot exceed 16000 characters.");
        }

        return output.ToString();
    }
}

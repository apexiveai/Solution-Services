using System.Text.Json;
using System.Text.Json.Nodes;
using Apexive.CoreRpa.Contracts;

namespace Apexive.CoreRpa.Cy.Runtime;

public sealed class CyWorkflowRuntime : IRuntimeEngine
{
    private const int MaxRules = 200;
    private const int MaxEvents = 100;
    private static readonly HashSet<string> Severities =
        ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"];

    public string Runtime => RuntimeNames.Cy;

    public ValueTask<RuntimeCompletion> ExecuteAsync(
        RuntimeJob job,
        CancellationToken cancellationToken = default)
    {
        ValidateJob(job);
        var rules = job.Definition.GetProperty("rules").EnumerateArray().ToArray();
        var events = job.InputData.TryGetProperty("events", out var eventArray)
            && eventArray.ValueKind == JsonValueKind.Array
                ? eventArray.EnumerateArray().ToArray()
                : throw new RuntimeContractException("CY input requires an events array.");
        if (rules.Length > MaxRules || events.Length > MaxEvents)
        {
            throw new RuntimeContractException(
                $"CY workflows are limited to {MaxRules} rules and {MaxEvents} input events.");
        }

        var alerts = new List<object>();
        foreach (var rule in rules)
        {
            cancellationToken.ThrowIfCancellationRequested();
            var field = RequiredString(rule, "field");
            foreach (var eventData in events)
            {
                if (TryGetPath(eventData, field, out var value)
                    && JsonElement.DeepEquals(value, rule.GetProperty("equals")))
                {
                    alerts.Add(new
                    {
                        rule_id = RequiredString(rule, "id"),
                        severity = RequiredString(rule, "severity"),
                        title = RequiredString(rule, "title"),
                        recommended_response = RequiredString(rule, "recommended_response"),
                    });
                }
            }
        }

        var result = JsonSerializer.SerializeToElement(new
        {
            alerts,
            requires_human_review = alerts.Count > 0,
        });
        return ValueTask.FromResult(new RuntimeCompletion("SUCCEEDED", result, null));
    }

    private static void ValidateJob(RuntimeJob job)
    {
        if (!string.Equals(job.Runtime, RuntimeNames.Cy, StringComparison.OrdinalIgnoreCase))
        {
            throw new RuntimeContractException("CY runtime received a job for another runtime.");
        }

        var definition = job.Definition;
        if (!string.Equals(RequiredString(definition, "runtime"), RuntimeNames.Cy, StringComparison.OrdinalIgnoreCase)
            || !definition.TryGetProperty("contract_version", out var contractVersion)
            || contractVersion.GetInt32() != RuntimeNames.ContractVersion
            || !definition.TryGetProperty("rules", out var rules)
            || rules.ValueKind != JsonValueKind.Array)
        {
            throw new RuntimeContractException("CY workflow definition does not match contract version 1.");
        }

        if (rules.GetArrayLength() > MaxRules)
        {
            throw new RuntimeContractException($"CY workflows may contain at most {MaxRules} rules.");
        }

        foreach (var rule in rules.EnumerateArray())
        {
            var properties = rule.EnumerateObject().Select(property => property.Name)
                .ToHashSet(StringComparer.Ordinal);
            if (!properties.SetEquals(
                    ["id", "field", "equals", "severity", "title", "recommended_response"]))
            {
                throw new RuntimeContractException("CY rule contains unsupported fields.");
            }

            _ = RequiredString(rule, "id");
            _ = RequiredString(rule, "title");
            _ = RequiredString(rule, "recommended_response");
            var severity = RequiredString(rule, "severity");
            if (!Severities.Contains(severity))
            {
                throw new RuntimeContractException($"CY severity '{severity}' is not supported.");
            }

            var field = RequiredString(rule, "field");
            if (field.Length > 120 || field.Split('.').Any(part =>
                    string.IsNullOrWhiteSpace(part)
                    || !part.All(character => char.IsAsciiLetterOrDigit(character) || character is '_' or '-')))
            {
                throw new RuntimeContractException("CY rule fields must be bounded dotted property names.");
            }
        }
    }

    private static bool TryGetPath(JsonElement element, string path, out JsonElement value)
    {
        value = element;
        foreach (var part in path.Split('.'))
        {
            if (value.ValueKind != JsonValueKind.Object
                || !value.TryGetProperty(part, out value))
            {
                return false;
            }
        }

        return true;
    }

    private static string RequiredString(JsonElement element, string property)
    {
        if (!element.TryGetProperty(property, out var value)
            || value.ValueKind != JsonValueKind.String
            || string.IsNullOrWhiteSpace(value.GetString()))
        {
            throw new RuntimeContractException($"CY rule requires a non-empty '{property}'.");
        }

        return value.GetString()!;
    }
}

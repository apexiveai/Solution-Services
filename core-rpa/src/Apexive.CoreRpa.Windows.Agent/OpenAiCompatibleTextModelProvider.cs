using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;
using Apexive.CoreRpa.Contracts;

namespace Apexive.CoreRpa.Windows.Agent;

public sealed class OpenAiCompatibleTextModelProvider : ITextModelProvider
{
    private const int MaxResponseCharacters = 32_000;
    private readonly HttpClient _httpClient;
    private readonly Uri _endpoint;
    private readonly string _model;
    private readonly string _apiKey;

    public OpenAiCompatibleTextModelProvider(HttpClient httpClient, IConfiguration configuration)
    {
        _httpClient = httpClient;
        var endpoint = configuration["CORE_RPA_AI_ENDPOINT"]
            ?? throw new InvalidOperationException("CORE_RPA_AI_ENDPOINT is required for AIS prompts.");
        if (!Uri.TryCreate(endpoint, UriKind.Absolute, out var parsedEndpoint)
            || (parsedEndpoint.Scheme != Uri.UriSchemeHttps
                && !(parsedEndpoint.IsLoopback && parsedEndpoint.Scheme == Uri.UriSchemeHttp)))
        {
            throw new InvalidOperationException(
                "CORE_RPA_AI_ENDPOINT must use HTTPS except for localhost development.");
        }
        _endpoint = parsedEndpoint;

        _model = configuration["CORE_RPA_AI_MODEL"]
            ?? throw new InvalidOperationException("CORE_RPA_AI_MODEL is required for AIS prompts.");
        _apiKey = configuration["CORE_RPA_AI_API_KEY"]
            ?? throw new InvalidOperationException("CORE_RPA_AI_API_KEY is required for AIS prompts.");
        if (string.IsNullOrWhiteSpace(_model) || string.IsNullOrWhiteSpace(_apiKey))
        {
            throw new InvalidOperationException(
                "CORE_RPA_AI_MODEL and CORE_RPA_AI_API_KEY cannot be empty.");
        }
    }

    public async ValueTask<string> CompleteAsync(
        string prompt,
        CancellationToken cancellationToken = default)
    {
        using var request = new HttpRequestMessage(HttpMethod.Post, _endpoint)
        {
            Content = JsonContent.Create(new
            {
                model = _model,
                messages = new[] { new { role = "user", content = prompt } },
            }),
        };
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", _apiKey);
        using var response = await _httpClient.SendAsync(request, cancellationToken);
        if (!response.IsSuccessStatusCode)
        {
            throw new HttpRequestException(
                $"Configured AIS model endpoint failed with {(int)response.StatusCode}.",
                null,
                response.StatusCode);
        }

        using var payload = await JsonDocument.ParseAsync(
            await response.Content.ReadAsStreamAsync(cancellationToken),
            cancellationToken: cancellationToken);
        if (!payload.RootElement.TryGetProperty("choices", out var choices)
            || choices.ValueKind != JsonValueKind.Array
            || choices.GetArrayLength() == 0
            || !choices[0].TryGetProperty("message", out var message)
            || !message.TryGetProperty("content", out var content)
            || content.ValueKind != JsonValueKind.String)
        {
            throw new JsonException("Configured AIS model endpoint returned no text completion.");
        }

        var result = content.GetString()
            ?? throw new JsonException("Configured AIS model endpoint returned an empty completion.");
        if (result.Length > MaxResponseCharacters)
        {
            throw new JsonException(
                $"AIS model completion exceeded the {MaxResponseCharacters}-character limit.");
        }

        return result;
    }
}

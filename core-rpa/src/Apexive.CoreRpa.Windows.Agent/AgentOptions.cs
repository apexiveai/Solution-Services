namespace Apexive.CoreRpa.Windows.Agent;

public sealed record AgentOptions(
    string ApiBaseUrl,
    string TokenUrl,
    string ClientId,
    string ClientSecret,
    Guid BotId,
    int PollIntervalSeconds)
{
    public static AgentOptions FromConfiguration(IConfiguration configuration)
    {
        var clientSecret = configuration["CORE_RPA_CLIENT_SECRET"]
            ?? throw new InvalidOperationException("CORE_RPA_CLIENT_SECRET is required.");
        var botIdValue = configuration["CORE_RPA_BOT_ID"];
        if (!Guid.TryParse(botIdValue, out var botId))
        {
            throw new InvalidOperationException("CORE_RPA_BOT_ID must be a UUID.");
        }

        var pollInterval = int.TryParse(configuration["CORE_RPA_POLL_INTERVAL_SECONDS"], out var parsed)
            ? parsed
            : 5;
        if (pollInterval is < 1 or > 60)
        {
            throw new InvalidOperationException("CORE_RPA_POLL_INTERVAL_SECONDS must be between 1 and 60.");
        }

        var options = new AgentOptions(
            Required(configuration, "CORE_RPA_API_BASE_URL"),
            Required(configuration, "CORE_RPA_TOKEN_URL"),
            Required(configuration, "CORE_RPA_CLIENT_ID"),
            clientSecret,
            botId,
            pollInterval);
        ValidateHttpsUrl(options.ApiBaseUrl, "CORE_RPA_API_BASE_URL");
        ValidateHttpsUrl(options.TokenUrl, "CORE_RPA_TOKEN_URL");
        return options;
    }

    private static string Required(IConfiguration configuration, string key) =>
        string.IsNullOrWhiteSpace(configuration[key])
            ? throw new InvalidOperationException($"{key} is required.")
            : configuration[key]!;

    private static void ValidateHttpsUrl(string value, string key)
    {
        if (!Uri.TryCreate(value, UriKind.Absolute, out var uri)
            || (uri.Scheme != Uri.UriSchemeHttps && !(uri.IsLoopback && uri.Scheme == Uri.UriSchemeHttp)))
        {
            throw new InvalidOperationException($"{key} must use HTTPS except for localhost development.");
        }
    }
}

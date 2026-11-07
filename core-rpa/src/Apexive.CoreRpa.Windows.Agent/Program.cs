using Apexive.CoreRpa.Ais.Runtime;
using Apexive.CoreRpa.Contracts;
using Apexive.CoreRpa.Cy.Runtime;
using Apexive.CoreRpa.Windows.Agent;

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddWindowsService(options => options.ServiceName = "Apexive CoreRPA Agent");
builder.Services.AddHttpClient<OrchestratorClient>(client =>
{
    client.Timeout = TimeSpan.FromSeconds(30);
});
builder.Services.AddHttpClient<OpenAiCompatibleTextModelProvider>(client =>
{
    client.Timeout = TimeSpan.FromMinutes(2);
    client.MaxResponseContentBufferSize = 1_000_000;
});
var aiConfiguration = new[]
{
    builder.Configuration["CORE_RPA_AI_ENDPOINT"],
    builder.Configuration["CORE_RPA_AI_MODEL"],
    builder.Configuration["CORE_RPA_AI_API_KEY"],
};
if (aiConfiguration.Any(value => value is not null))
{
    if (aiConfiguration.Any(string.IsNullOrWhiteSpace))
    {
        throw new InvalidOperationException(
            "Configure CORE_RPA_AI_ENDPOINT, CORE_RPA_AI_MODEL and CORE_RPA_AI_API_KEY together.");
    }
    builder.Services.AddSingleton<ITextModelProvider>(
        provider => provider.GetRequiredService<OpenAiCompatibleTextModelProvider>());
}
builder.Services.AddSingleton(AgentOptions.FromConfiguration(builder.Configuration));
builder.Services.AddSingleton(provider =>
    new RuntimeEngine(
    [
        new AisWorkflowRuntime(provider.GetService<ITextModelProvider>()),
        new CyWorkflowRuntime(),
    ]));
builder.Services.AddHostedService<AgentWorker>();

await builder.Build().RunAsync();

# Apexive CoreRPA Studios and Windows Agent

This workspace adds versioned AIS and CY runtime projects alongside the existing
CoreRPA backend and web orchestrator. It does not replace the existing CoreRPA
workflow engine or licensing module.

## Compatibility and licensing boundary

- Workflows without a `runtime` field remain CoreRPA workflows and keep using
  the existing bounded Python runtime.
- AIS and CY workflows opt into contract version 1 with `"runtime": "AIS"` or
  `"runtime": "CY"`.
- Workflow creation, execution requests, approvals, audit events, bot limits,
  monthly execution limits, active-license checks and the license purchase and
  activation lifecycle continue through the existing `/api/v1/automation` and
  `/api/v1/core-rpa` APIs.
- AIS/CY execution claims recheck the active tenant license. The separate
  `core_rpa_agent` service role is limited to registering, starting, heartbeating
  and claiming work for its own AIS/CY bots.
- The default CoreRPA worker explicitly skips AIS/CY work; it will not attempt
  to interpret the studio-specific definitions.
- Studio agent claims use the existing queue `attempts` field as a fencing
  counter. A completion from an expired claim is rejected after a stale agent
  lease is recovered.
- CY rules evaluate supplied event records and emit alerts plus response
  recommendations. They do not scan systems or execute security actions.

The shared JSON contract is `contracts/workflow-v1.schema.json`. The C# contract
library and runtime engines are in `src/`; the studio pages live at `/ais-studio`
and `/cy-studio` in the existing Next.js application.

## Runtime test/build

From the repository root:

```powershell
dotnet test .\core-rpa\tests\Apexive.CoreRpa.Runtime.Tests\Apexive.CoreRpa.Runtime.Tests.csproj
dotnet build .\core-rpa\src\Apexive.CoreRpa.Windows.Agent\Apexive.CoreRpa.Windows.Agent.csproj
```

The backend regression tests are run from `backend\`:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_automation tests.test_licensing
```

## Agent provisioning

Create a Keycloak client-credentials identity with the tenant claim and the
`core_rpa_agent` role. Register its bot through the existing
`POST /api/v1/automation/bots` route using only `runtime:AIS` and/or
`runtime:CY` capabilities. Use that same client identity for the installed
agent; the backend binds the bot to the identity that registered it.

Configure these machine environment variables before starting the Windows
service:

- `CORE_RPA_API_BASE_URL`: backend origin, HTTPS in production.
- `CORE_RPA_TOKEN_URL`: Keycloak token endpoint, HTTPS in production.
- `CORE_RPA_CLIENT_ID` and `CORE_RPA_CLIENT_SECRET`: service client credentials.
- `CORE_RPA_BOT_ID`: UUID of the licensed bot registered for this identity.
- `CORE_RPA_POLL_INTERVAL_SECONDS`: optional value from 1 to 60 (default 5).

For AIS prompt steps, configure all three additional variables:
`CORE_RPA_AI_ENDPOINT` (an administrator-selected OpenAI-compatible HTTPS
endpoint), `CORE_RPA_AI_MODEL`, and `CORE_RPA_AI_API_KEY`. The agent sends the
expanded prompt and supplied workflow data to this configured endpoint. Do not
configure a provider unless the tenant has approved that data-processing
destination. Without a configured provider, prompt tasks fail explicitly.

The service uses the Windows `LocalService` account. The MSI does not contain
tenant credentials or start the service during installation. Provision
environment variables through the organization's approved secret-management
process before starting the service; do not put credentials in the repository
or MSI command line.

## Windows MSI

`windows\build-msi.ps1` publishes a self-contained `win-x64` service and builds
the WiX MSI. A production build requires a trusted code-signing certificate
installed on the build host:

```powershell
.\core-rpa\windows\build-msi.ps1 -Version "1.0.0" -CertificateThumbprint "<certificate-thumbprint>"
```

For local packaging checks only, `-SkipSigning` produces an unsigned MSI. It is
not suitable for production distribution. A production release still requires
the organization's signing certificate, release approval and Windows install
testing.

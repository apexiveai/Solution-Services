param(
    [string]$Version = "1.0.0",
    [string]$CertificateThumbprint,
    [switch]$SkipSigning
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$agentProject = Join-Path $root "src\Apexive.CoreRpa.Windows.Agent\Apexive.CoreRpa.Windows.Agent.csproj"
$setupProject = Join-Path $PSScriptRoot "Apexive.CoreRpa.Agent.Setup\Apexive.CoreRpa.Agent.Setup.wixproj"
$publishDirectory = Join-Path $root "publish\win-x64"
if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Version must use the MSI-compatible major.minor.patch format."
}
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw "WiX installer validation requires an elevated Administrator session."
}
if (-not $SkipSigning) {
    if ([string]::IsNullOrWhiteSpace($CertificateThumbprint)) {
        throw "Production MSI signing requires -CertificateThumbprint; use -SkipSigning only for local testing."
    }
    $certificate = Get-ChildItem "Cert:\LocalMachine\My", "Cert:\CurrentUser\My" `
        -ErrorAction SilentlyContinue |
        Where-Object { $_.Thumbprint -eq $CertificateThumbprint -and $_.HasPrivateKey } |
        Select-Object -First 1
    if ($null -eq $certificate) {
        throw "A signing certificate with a private key was not found in the current-user or local-machine store."
    }
    if ($null -eq (Get-Command signtool.exe -ErrorAction SilentlyContinue)) {
        throw "Windows SDK signtool.exe is required to sign the production MSI."
    }
}

& dotnet publish $agentProject --configuration Release --runtime win-x64 --self-contained true `
    -p:PublishSingleFile=true -o $publishDirectory
if ($LASTEXITCODE -ne 0) {
    throw "Windows Agent publish failed with exit code $LASTEXITCODE."
}

& dotnet build $setupProject --configuration Release `
    "-p:AgentPublishDir=$publishDirectory" "-p:PackageVersion=$Version"
if ($LASTEXITCODE -ne 0) {
    throw "Windows MSI build failed with exit code $LASTEXITCODE."
}

$msi = Join-Path $PSScriptRoot "Apexive.CoreRpa.Agent.Setup\bin\Release\Apexive.CoreRpa.Agent.Setup.msi"
if (-not (Test-Path $msi)) {
    throw "The MSI build completed without producing the expected installer: $msi"
}

if (-not $SkipSigning) {
    $signTool = Get-Command signtool.exe -ErrorAction SilentlyContinue
    & $signTool.Source sign /sha1 $CertificateThumbprint /fd SHA256 `
        /tr http://timestamp.digicert.com /td SHA256 $msi
    if ($LASTEXITCODE -ne 0) {
        throw "MSI signing failed with exit code $LASTEXITCODE."
    }
}

Write-Output $msi

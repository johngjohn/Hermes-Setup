param(
    [string]$SshExe = "${SSH_EXE_PATH}",
    [string]$LogFile = "${SSH_LOG_PATH}",
    [string]$VpsHost = "${VPS_HOST}",
    [int]$VpsSshPort = ${VPS_SSH_PORT},
    [string]$VpsUser = "${VPS_USER}",
    [int]$VpsRemotePort = ${VPS_REMOTE_PORT},
    [int]$ObsidianLocalPort = ${OBSIDIAN_LOCAL_PORT},
    [int]$RetrySeconds = 5
)

$ErrorActionPreference = 'Stop'
$script:StopRequested = $false

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $line = "[$timestamp] $Message"
    Write-Host $line
    if ($LogFile) {
        $directory = Split-Path -Parent $LogFile
        if ($directory) {
            New-Item -Path $directory -ItemType Directory -Force -ErrorAction SilentlyContinue | Out-Null
        }
        Add-Content -Path $LogFile -Value $line
    }
}

if (-not (Test-Path -Path $SshExe)) {
    throw "ssh.exe not found at $SshExe. Install the Windows OpenSSH Client or update -SshExe."
}

$TunnelTarget = "ssh -N -R 127.0.0.1:$VpsRemotePort:127.0.0.1:$ObsidianLocalPort -p $VpsSshPort $VpsUser@$VpsHost"
Write-Log "Starting reverse SSH loop."
Write-Log "Exact reverse tunnel target: $TunnelTarget"
Write-Log "Press Ctrl+C to stop the loop."

$null = Register-EngineEvent -SourceIdentifier ConsoleBreak -Action {
    $script:StopRequested = $true
}

try {
    while (-not $script:StopRequested) {
        Write-Log "Launching ssh.exe."
        & $SshExe -N -R "127.0.0.1:$VpsRemotePort:127.0.0.1:$ObsidianLocalPort" -p $VpsSshPort "$VpsUser@$VpsHost"
        $exitCode = $LASTEXITCODE
        if ($script:StopRequested) {
            break
        }
        Write-Log "ssh.exe exited with code $exitCode. Sleeping $RetrySeconds seconds before retry."
        Start-Sleep -Seconds $RetrySeconds
    }
}
catch {
    if ($_.FullyQualifiedErrorId -eq 'PipelineStopped') {
        $script:StopRequested = $true
    }
    else {
        Write-Log "Fatal error: $($_.Exception.Message)"
        throw
    }
}
finally {
    Write-Log "Reverse SSH loop stopped."
}

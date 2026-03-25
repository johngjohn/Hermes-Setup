param(
    [int]$$LocalPort = ${OBSIDIAN_LOCAL_PORT},
    [string]$$ApiKey = $$env:OBSIDIAN_API_KEY
)

$$ErrorActionPreference = 'Stop'
$$TargetHost = '127.0.0.1'
$$Url = "http://$$TargetHost`:$$LocalPort/mcp"

if (-not $$ApiKey) {
    $$secureApiKey = Read-Host -Prompt "Obsidian API key" -AsSecureString
    $$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($$secureApiKey)
    try {
        $$ApiKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($$bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($$bstr)
    }
}

if (-not $$ApiKey) {
    Write-Host "[error] Missing Obsidian API key. Set OBSIDIAN_API_KEY or provide it at prompt."
    exit 2
}

Write-Host "[info] Testing TCP on $$TargetHost:$$LocalPort"
$$tcp = Test-NetConnection -ComputerName $$TargetHost -Port $$LocalPort -WarningAction SilentlyContinue
if (-not $$tcp.TcpTestSucceeded) {
    Write-Host "[warn] TCP connection failed. Likely causes: Obsidian closed, plugin disabled, wrong port."
    exit 1
}

Write-Host "[info] Calling authenticated MCP endpoint at $$Url"
try {
    $$response = Invoke-WebRequest -Uri $$Url -Method Get -Headers @{ Authorization="Bearer $$ApiKey" } -TimeoutSec 15 -UseBasicParsing
    Write-Host "[ok] HTTP status: $$($$response.StatusCode)"
}
catch {
    if ($$_.Exception.Response) {
        $$statusCode = [int]$$_.Exception.Response.StatusCode
        Write-Host "[warn] HTTP status: $$statusCode"
        if ($$statusCode -eq 401 -or $$statusCode -eq 403) {
            Write-Host "[warn] Wrong Obsidian API key or unauthorized client."
        }
        else {
            Write-Host "[warn] Plugin answered, but with a non-success status."
        }
        exit 1
    }
    Write-Host "[warn] Request failed. Likely causes: Obsidian closed, plugin disabled, wrong key, wrong port."
    exit 1
}

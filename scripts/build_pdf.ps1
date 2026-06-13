$ErrorActionPreference = "Continue"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$DataDir = Join-Path $Root "data"
$DownloadsPdf = "C:/Users/wangz/Downloads/35.pdf"
$StatusPath = Join-Path $DataDir "build_status.json"

if (!(Test-Path $DataDir)) {
    New-Item -ItemType Directory -Path $DataDir | Out-Null
}

$status = [ordered]@{
    status = "started"
    paper_dir = $Root
    downloads_pdf = $DownloadsPdf
    steps = @()
    copied = $false
    removed_local_pdf = $false
}

function Add-Step {
    param(
        [string]$Name,
        [int]$Code,
        [string]$LogPath
    )
    $script:status.steps += [ordered]@{
        name = $Name
        exit_code = $Code
        log = $LogPath
    }
}

function Run-Tool {
    param(
        [string]$Name,
        [string]$Exe,
        [string[]]$ArgList
    )
    $logPath = Join-Path $Root ("build_" + $Name + ".log")
    Push-Location $Root
    try {
        & $Exe @ArgList *> $logPath
        $code = $LASTEXITCODE
        if ($null -eq $code) { $code = 0 }
    } catch {
        $_.Exception.Message | Set-Content -Path $logPath -Encoding UTF8
        $code = 1
    } finally {
        Pop-Location
    }
    Add-Step -Name $Name -Code $code -LogPath $logPath
    return $code
}

$ok = $true
if (!(Test-Path (Join-Path $Root "main.tex"))) {
    $status.status = "failed"
    $status.error = "main.tex does not exist"
    $ok = $false
}

if ($ok) {
    $code = Run-Tool -Name "pdflatex1" -Exe "pdflatex" -ArgList @("-interaction=nonstopmode", "-halt-on-error", "main.tex")
    if ($code -ne 0) { $ok = $false }
}
if ($ok) {
    $code = Run-Tool -Name "pdflatex2" -Exe "pdflatex" -ArgList @("-interaction=nonstopmode", "-halt-on-error", "main.tex")
    if ($code -ne 0) { $ok = $false }
}
if ($ok -and (Test-Path (Join-Path $Root "main.pdf"))) {
    try {
        $localPdf = Join-Path $Root "main.pdf"
        Copy-Item -Path $localPdf -Destination $DownloadsPdf -Force
        Remove-Item -LiteralPath $localPdf -Force
        $status.status = "complete"
        $status.copied = $true
        $status.removed_local_pdf = $true
    } catch {
        $status.status = "copy_failed"
        $status.error = $_.Exception.Message
    }
} elseif ($ok) {
    $status.status = "failed"
    $status.error = "pdflatex completed but main.pdf is missing"
} else {
    if (!$status.Contains("status") -or $status.status -eq "started") {
        $status.status = "failed"
    }
    if (!$status.Contains("error")) {
        $status.error = "one or more LaTeX steps failed"
    }
}

$status | ConvertTo-Json -Depth 5 | Set-Content -Path $StatusPath -Encoding UTF8
exit 0

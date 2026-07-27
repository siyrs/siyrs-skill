param(
    [string]$SkillSource = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$ClaudeHome = (Join-Path $HOME ".claude")
)

$ErrorActionPreference = "Stop"
$skillTarget = Join-Path $ClaudeHome "skills\siyrs-skill"
$commandTarget = Join-Path $ClaudeHome "commands"

New-Item -ItemType Directory -Force -Path (Split-Path $skillTarget) | Out-Null
New-Item -ItemType Directory -Force -Path $commandTarget | Out-Null

$sourceFull = [System.IO.Path]::GetFullPath([string]$SkillSource).TrimEnd('\', '/')
$targetFull = [System.IO.Path]::GetFullPath($skillTarget).TrimEnd('\', '/')
if ($sourceFull -ne $targetFull) {
    $tempTarget = "$skillTarget.tmp.$PID"
    try {
        if (Test-Path $tempTarget) {
            Remove-Item -Recurse -Force $tempTarget
        }
        Copy-Item -Recurse -Force $sourceFull $tempTarget
        foreach ($relative in @(".git", "__pycache__", ".pytest_cache")) {
            $candidate = Join-Path $tempTarget $relative
            if (Test-Path $candidate) {
                Remove-Item -Recurse -Force $candidate
            }
        }
        Get-ChildItem -Path $tempTarget -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force
        Get-ChildItem -Path $tempTarget -File -Recurse -Include "*.pyc", "*.pyo" -ErrorAction SilentlyContinue |
            Remove-Item -Force
        if (Test-Path $skillTarget) {
            Remove-Item -Recurse -Force $skillTarget
        }
        Move-Item -Force $tempTarget $skillTarget
    }
    finally {
        if (Test-Path $tempTarget) {
            Remove-Item -Recurse -Force $tempTarget
        }
    }
}
Copy-Item -Force (Join-Path $PSScriptRoot "commands\*.md") $commandTarget

Write-Host "Installed siyrs-skill to $skillTarget"
Write-Host "Installed /siyk-* command adapters to $commandTarget"

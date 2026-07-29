param(
    [string]$SkillSource = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$ClaudeHome = (Join-Path $HOME ".claude"),
    [string]$Python = "python"
)
$ErrorActionPreference = "Stop"
$sourceFull = [System.IO.Path]::GetFullPath([string]$SkillSource).TrimEnd('\','/')
$registry = Join-Path $sourceFull "scripts\command_registry.py"
$names = @(& $Python $registry --root $sourceFull --field names)
$legacyNames = @(& $Python $registry --root $sourceFull --field legacy-names)
if ($LASTEXITCODE -ne 0) { throw "Unable to read command registry" }
$skillTarget = Join-Path $ClaudeHome "skills\siyrs-skill"
$commandTarget = Join-Path $ClaudeHome "commands"
New-Item -ItemType Directory -Force -Path (Split-Path $skillTarget), $commandTarget | Out-Null
$targetFull = [System.IO.Path]::GetFullPath($skillTarget).TrimEnd('\','/')
if ($sourceFull -ne $targetFull) {
    $tempTarget = "$skillTarget.tmp.$PID"
    try {
        if (Test-Path $tempTarget) { Remove-Item -Recurse -Force $tempTarget }
        Copy-Item -Recurse -Force $sourceFull $tempTarget
        foreach ($relative in @(".git","__pycache__",".pytest_cache")) { $p=Join-Path $tempTarget $relative; if(Test-Path $p){Remove-Item -Recurse -Force $p} }
        Get-ChildItem $tempTarget -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
        Get-ChildItem $tempTarget -File -Recurse -Include "*.pyc","*.pyo" -ErrorAction SilentlyContinue | Remove-Item -Force
        if (Test-Path $skillTarget) { Remove-Item -Recurse -Force $skillTarget }
        Move-Item -Force $tempTarget $skillTarget
    } finally { if(Test-Path $tempTarget){Remove-Item -Recurse -Force $tempTarget} }
}
foreach ($name in @($names)+@($legacyNames)) { $p=Join-Path $commandTarget "$name.md"; if(Test-Path $p){Remove-Item -Force $p} }
Get-ChildItem $commandTarget -File -Filter "siyk-*.md" -ErrorAction SilentlyContinue | ForEach-Object {
    if ((Get-Content -Raw $_.FullName) -match "(?m)^siyrs-skill-command-adapter:\s*true\s*$") { Remove-Item -Force $_.FullName }
}
foreach ($name in $names) { Copy-Item -Force (Join-Path $PSScriptRoot "commands\$name.md") (Join-Path $commandTarget "$name.md") }
Write-Host "Installed siyrs-skill and commands: $($names -join ', ')"

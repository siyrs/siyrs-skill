param(
    [string]$SkillSource = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$ClaudeHome = (Join-Path $HOME ".claude"),
    [string]$Python = "python"
)
$ErrorActionPreference = "Stop"
$sourceFull = [IO.Path]::GetFullPath([string]$SkillSource).TrimEnd('\','/')
$skillTarget = Join-Path $ClaudeHome "skills\siyrs-skill"
$commandTarget = Join-Path $ClaudeHome "commands"
$registry = Join-Path $sourceFull "scripts\command_registry.py"
$names = @(& $Python $registry --root $sourceFull --field names)
$legacyNames = @(& $Python $registry --root $sourceFull --field legacy-names)
if ($LASTEXITCODE -ne 0) { throw "Unable to read command registry" }
New-Item -ItemType Directory -Force -Path (Split-Path $skillTarget), $commandTarget | Out-Null
$targetFull = [IO.Path]::GetFullPath($skillTarget).TrimEnd('\','/')
if (-not [string]::Equals($sourceFull, $targetFull, [StringComparison]::OrdinalIgnoreCase)) {
    $temp = "$skillTarget.tmp.$PID"
    try {
        if (Test-Path $temp) { Remove-Item -Recurse -Force $temp }
        Copy-Item -Recurse -Force $sourceFull $temp
        foreach ($relative in @('.git','__pycache__','.pytest_cache')) {
            $candidate = Join-Path $temp $relative
            if (Test-Path $candidate) { Remove-Item -Recurse -Force $candidate }
        }
        Get-ChildItem $temp -Directory -Recurse -Filter '__pycache__' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
        Get-ChildItem $temp -File -Recurse -Include '*.pyc','*.pyo' -ErrorAction SilentlyContinue | Remove-Item -Force
        if (Test-Path $skillTarget) { Remove-Item -Recurse -Force $skillTarget }
        Move-Item $temp $skillTarget
    } finally { if (Test-Path $temp) { Remove-Item -Recurse -Force $temp } }
}
foreach ($name in @($names + $legacyNames)) {
    $path = Join-Path $commandTarget "$name.md"
    if (Test-Path $path) { Remove-Item -Force $path }
}
Get-ChildItem $commandTarget -File -Filter 'siyk-*.md' -ErrorAction SilentlyContinue | ForEach-Object {
    if ((Get-Content -Raw $_.FullName) -match '(?m)^siyrs-skill-command-adapter:\s*true\s*$') { Remove-Item -Force $_.FullName }
}
foreach ($name in $names) {
    Copy-Item -Force (Join-Path $PSScriptRoot "commands\$name.md") (Join-Path $commandTarget "$name.md")
}
Write-Host "Installed siyrs-skill and commands: $($names -join ', ')"

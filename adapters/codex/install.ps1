param(
    [string]$SkillSource = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$SkillsHome = (Join-Path $HOME ".agents\skills"),
    [string]$LegacyArchiveHome
)

$ErrorActionPreference = "Stop"
$entrypoints = @("siyk-test-full", "siyk-test-new", "siyk-git-commit", "siyk-git-sync")
$sourceFull = [System.IO.Path]::GetFullPath([string]$SkillSource).TrimEnd('\', '/')
$skillsHomeFull = [System.IO.Path]::GetFullPath($SkillsHome).TrimEnd('\', '/')
$archiveHomeFull = if ([string]::IsNullOrWhiteSpace($LegacyArchiveHome)) {
    Join-Path (Split-Path -Parent $skillsHomeFull) "skill-backups"
}
else {
    [System.IO.Path]::GetFullPath($LegacyArchiveHome).TrimEnd('\', '/')
}

function Test-PathInside {
    param([string]$Path, [string]$Parent)
    $normalizedPath = [System.IO.Path]::GetFullPath($Path).TrimEnd('\', '/')
    $normalizedParent = [System.IO.Path]::GetFullPath($Parent).TrimEnd('\', '/')
    return [string]::Equals($normalizedPath, $normalizedParent, [System.StringComparison]::OrdinalIgnoreCase) -or
        $normalizedPath.StartsWith($normalizedParent + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)
}

function Test-SiyrsSkillManifest {
    param([string]$Directory)
    $manifest = Join-Path $Directory "SKILL.md"
    return (Test-Path -LiteralPath $manifest) -and
        ((Get-Content -Raw -LiteralPath $manifest) -match "(?m)^name:\s*siyrs-skill\s*$")
}

New-Item -ItemType Directory -Force -Path $skillsHomeFull | Out-Null
if ($skillsHomeFull.StartsWith($sourceFull + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to install inside the source repository: $skillsHomeFull"
}
if (Test-PathInside -Path $archiveHomeFull -Parent $skillsHomeFull) {
    throw "Legacy archive location must be outside the Codex Skills discovery directory: $archiveHomeFull"
}

$coreTarget = Join-Path $skillsHomeFull "siyrs-skill"
$archivedLegacy = @()
$reservedNames = @("siyrs-skill") + $entrypoints
foreach ($candidate in Get-ChildItem -Force -LiteralPath $skillsHomeFull -Directory) {
    if ($candidate.Name -in $reservedNames -or -not (Test-SiyrsSkillManifest -Directory $candidate.FullName)) {
        continue
    }
    New-Item -ItemType Directory -Force -Path $archiveHomeFull | Out-Null
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $archiveTarget = Join-Path $archiveHomeFull ("siyrs-skill-duplicate-{0}" -f $stamp)
    $suffix = 1
    while (Test-Path -LiteralPath $archiveTarget) {
        $archiveTarget = Join-Path $archiveHomeFull ("siyrs-skill-duplicate-{0}-{1}" -f $stamp, $suffix)
        $suffix += 1
    }
    Move-Item -LiteralPath $candidate.FullName -Destination $archiveTarget
    $archivedLegacy += $archiveTarget
}

$installCore = $true
if (Test-Path -LiteralPath $coreTarget) {
    $coreReal = [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $coreTarget)).TrimEnd('\', '/')
    if ([string]::Equals($coreReal, $sourceFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        $installCore = $false
    }
}

$stageRoot = Join-Path $skillsHomeFull (".siyrs-codex-install.{0}.{1}" -f $PID, [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $stageRoot | Out-Null

try {
    if ($installCore) {
        $coreStage = Join-Path $stageRoot "siyrs-skill"
        New-Item -ItemType Directory -Force -Path $coreStage | Out-Null
        Get-ChildItem -Force -LiteralPath $sourceFull |
            Where-Object { $_.Name -notin @(".git", "__pycache__", ".pytest_cache") } |
            Copy-Item -Destination $coreStage -Recurse -Force
        foreach ($relative in @(".git", "__pycache__", ".pytest_cache")) {
            $candidate = Join-Path $coreStage $relative
            if (Test-Path -LiteralPath $candidate) { Remove-Item -Recurse -Force -LiteralPath $candidate }
        }
        Get-ChildItem -Path $coreStage -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force
        Get-ChildItem -Path $coreStage -File -Recurse -Include "*.pyc", "*.pyo" -ErrorAction SilentlyContinue |
            Remove-Item -Force
    }

    foreach ($name in $entrypoints) {
        $sourceDir = Join-Path $PSScriptRoot ("entrypoints\" + $name)
        $template = Join-Path $sourceDir "SKILL.template.md"
        if (-not (Test-Path -LiteralPath $template)) { throw "Missing entrypoint template: $template" }
        $targetStage = Join-Path $stageRoot $name
        New-Item -ItemType Directory -Force -Path $targetStage | Out-Null
        Copy-Item -Force -LiteralPath $template -Destination (Join-Path $targetStage "SKILL.md")
        $agents = Join-Path $sourceDir "agents"
        if (Test-Path -LiteralPath $agents) { Copy-Item -Recurse -Force -LiteralPath $agents -Destination $targetStage }
        $content = Get-Content -Raw -LiteralPath (Join-Path $targetStage "SKILL.md")
        if ($content -notmatch "(?m)^name:\s*$([regex]::Escape($name))\s*$") {
            throw "Invalid entrypoint name in $template"
        }
    }

    $namesToInstall = @()
    if ($installCore) { $namesToInstall += "siyrs-skill" }
    $namesToInstall += $entrypoints

    foreach ($name in $namesToInstall) {
        $target = Join-Path $skillsHomeFull $name
        if (Test-Path -LiteralPath $target) { Remove-Item -Recurse -Force -LiteralPath $target }
        Move-Item -Force -LiteralPath (Join-Path $stageRoot $name) -Destination $target
    }
}
finally {
    if (Test-Path -LiteralPath $stageRoot) { Remove-Item -Recurse -Force -LiteralPath $stageRoot }
}

$legacy = Join-Path $HOME ".codex\skills\siyrs-skill"
if (Test-Path -LiteralPath $legacy) {
    Write-Warning "Legacy Codex Skill found at $legacy; remove it manually after verifying the new install."
}

Write-Host "Installed siyrs-skill core to $coreTarget"
Write-Host "Installed Codex entrypoints: $($entrypoints -join ', ')"
if ($archivedLegacy.Count -gt 0) {
    Write-Host "Archived duplicate siyrs-skill copies: $($archivedLegacy -join ', ')"
}
Write-Host "Restart Codex if /siyk autocomplete does not refresh immediately."

param(
    [string]$SkillSource = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$SkillsHome = (Join-Path $HOME ".agents\skills"),
    [string]$LegacyArchiveHome,
    [string]$Python = "python"
)
$ErrorActionPreference = "Stop"
$sourceFull = [IO.Path]::GetFullPath([string]$SkillSource).TrimEnd('\','/')
$skillsHomeFull = [IO.Path]::GetFullPath($SkillsHome).TrimEnd('\','/')
$archiveHomeFull = if ([string]::IsNullOrWhiteSpace($LegacyArchiveHome)) { Join-Path (Split-Path -Parent $skillsHomeFull) "skill-backups" } else { [IO.Path]::GetFullPath($LegacyArchiveHome).TrimEnd('\','/') }
$registry = Join-Path $sourceFull "scripts\command_registry.py"
$entrypoints = @(& $Python $registry --root $sourceFull --field names)
$legacyNames = @(& $Python $registry --root $sourceFull --field legacy-names)
if ($LASTEXITCODE -ne 0) { throw "Unable to read command registry" }
function Test-Inside([string]$Path,[string]$Parent) {
    $p=[IO.Path]::GetFullPath($Path).TrimEnd('\','/');$q=[IO.Path]::GetFullPath($Parent).TrimEnd('\','/')
    return $p -eq $q -or $p.StartsWith($q+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)
}
if (Test-Inside $skillsHomeFull $sourceFull) { throw "Refusing install inside source" }
if (Test-Inside $archiveHomeFull $skillsHomeFull) { throw "Archive must be outside discovery directory" }
New-Item -ItemType Directory -Force -Path $skillsHomeFull,$archiveHomeFull | Out-Null
function Archive([string]$Path,[string]$Label) {
    if (-not (Test-Path -LiteralPath $Path)) { return }
    $stamp=Get-Date -Format 'yyyyMMdd-HHmmss';$target=Join-Path $archiveHomeFull "$Label-$stamp";$i=1
    while (Test-Path -LiteralPath $target) { $target=Join-Path $archiveHomeFull "$Label-$stamp-$i";$i++ }
    Move-Item -LiteralPath $Path -Destination $target
}
$coreTarget=Join-Path $skillsHomeFull 'siyrs-skill'
foreach ($candidate in Get-ChildItem -Force -LiteralPath $skillsHomeFull -Directory) {
    if ($candidate.Name -eq 'siyrs-skill') { continue }
    $manifest=Join-Path $candidate.FullName 'SKILL.md'
    if ((Test-Path $manifest) -and ((Get-Content -Raw $manifest) -match '(?m)^name:\s*siyrs-skill\s*$')) { Archive $candidate.FullName 'siyrs-skill-duplicate' }
}
foreach ($name in $legacyNames) { Archive (Join-Path $skillsHomeFull $name) "siyrs-entrypoint-$name" }
$stage=Join-Path $skillsHomeFull ('.siyrs-codex-install.{0}.{1}' -f $PID,[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force $stage | Out-Null
try {
    $installCore=$true
    if (Test-Path $coreTarget) {
        $coreReal=[IO.Path]::GetFullPath((Resolve-Path $coreTarget)).TrimEnd('\','/')
        if ([string]::Equals($coreReal,$sourceFull,[StringComparison]::OrdinalIgnoreCase)) { $installCore=$false }
    }
    if ($installCore) {
        $dst=Join-Path $stage 'siyrs-skill';New-Item -ItemType Directory -Force $dst | Out-Null
        Get-ChildItem -Force $sourceFull | Where-Object {$_.Name -notin @('.git','__pycache__','.pytest_cache')} | Copy-Item -Destination $dst -Recurse -Force
    }
    foreach ($name in $entrypoints) {
        $src=Join-Path $PSScriptRoot "entrypoints\$name";$template=Join-Path $src 'SKILL.template.md'
        if (-not (Test-Path $template)) { throw "Missing $template" }
        $dst=Join-Path $stage $name;New-Item -ItemType Directory -Force $dst | Out-Null
        Copy-Item $template (Join-Path $dst 'SKILL.md')
        if (Test-Path (Join-Path $src 'agents')) { Copy-Item -Recurse (Join-Path $src 'agents') (Join-Path $dst 'agents') }
    }
    $names=@();if($installCore){$names+='siyrs-skill'};$names+=$entrypoints
    foreach($name in $names){$target=Join-Path $skillsHomeFull $name;if(Test-Path $target){Remove-Item -Recurse -Force $target};Move-Item (Join-Path $stage $name) $target}
} finally { if (Test-Path $stage) { Remove-Item -Recurse -Force $stage } }
Write-Host "Installed siyrs-skill and entrypoints: $($entrypoints -join ', ')"

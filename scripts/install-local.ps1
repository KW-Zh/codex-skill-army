[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$CodexHome = "$env:USERPROFILE\.codex",
    [switch]$ConfirmOverwrite
)

# Supports PowerShell -WhatIf. No overwrite by default.
$ErrorActionPreference = "Stop"

$source = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$codexHomeResolved = [System.IO.Path]::GetFullPath($CodexHome)
$skillsRoot = [System.IO.Path]::GetFullPath((Join-Path $codexHomeResolved "skills"))
$target = [System.IO.Path]::GetFullPath((Join-Path $skillsRoot "codex-skill-army"))

if (-not $target.StartsWith($skillsRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Target path is outside the Codex skills directory: $target"
}

$files = Get-ChildItem -LiteralPath $source -Recurse -File | Where-Object {
    $_.FullName -notmatch "\\(__pycache__|\.git|node_modules)\\"
}

$planned = foreach ($file in $files) {
    $sourcePrefix = $source.TrimEnd("\") + "\"
    $relative = $file.FullName.Substring($sourcePrefix.Length)
    $destination = Join-Path $target $relative
    [PSCustomObject]@{
        Source = $file.FullName
        Destination = $destination
        Exists = Test-Path -LiteralPath $destination
    }
}

$conflicts = @($planned | Where-Object { $_.Exists })
if ($conflicts.Count -gt 0 -and -not $ConfirmOverwrite) {
    Write-Host "Install aborted: target already has files with the same names. Default is no overwrite."
    $conflicts | Select-Object Destination | Format-Table -AutoSize
    throw "After manual review, rerun with -ConfirmOverwrite if you intentionally want to overwrite."
}

if ($ConfirmOverwrite -and $conflicts.Count -gt 0) {
    Write-Host "The following files will be overwritten:"
    $conflicts | Select-Object Destination | Format-Table -AutoSize
    $answer = Read-Host "Type YES to confirm overwrite"
    if ($answer -ne "YES") {
        throw "Overwrite was not confirmed. Install aborted."
    }
}

foreach ($item in $planned) {
    if ($PSCmdlet.ShouldProcess($item.Destination, "Copy codex-skill-army file")) {
        New-Item -ItemType Directory -Force -Path (Split-Path $item.Destination) | Out-Null
        Copy-Item -LiteralPath $item.Source -Destination $item.Destination -Force:$ConfirmOverwrite
    }
}

if ($WhatIfPreference) {
    Write-Host "Dry run complete for $target. No files were copied."
} else {
    Write-Host "Installed to $target. Restart Codex before using the skill."
}

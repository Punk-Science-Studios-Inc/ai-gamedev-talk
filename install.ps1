# Copies agents/ and skills/ into each harness directory. Writes only its own entries. Deletes nothing else.
param([string[]]$Target = @((Join-Path $HOME '.agents'), (Join-Path $HOME '.claude')))
$here = $PSScriptRoot
foreach ($t in $Target) {
  New-Item -ItemType Directory -Force -Path (Join-Path $t 'agents'), (Join-Path $t 'skills') | Out-Null
  Get-ChildItem (Join-Path $here 'agents') -Filter *.md | Copy-Item -Destination (Join-Path $t 'agents') -Force
  foreach ($d in Get-ChildItem (Join-Path $here 'skills') -Directory) {
    $dst = Join-Path $t "skills\$($d.Name)"
    if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
    Copy-Item $d.FullName $dst -Recurse
  }
  Write-Host "installed into $t"
}

$workspace = (Resolve-Path -LiteralPath 'E:\agent\mwangLab').Path
$archive = Join-Path $workspace 'archive'
$runtimeArchive = Join-Path $archive 'runtime'
$benchmarkArchive = Join-Path $archive 'benchmarks'
$historicalArchive = Join-Path $archive 'historical'
New-Item -ItemType Directory -Force -Path $runtimeArchive, $benchmarkArchive, $historicalArchive | Out-Null

$targets = @(
    @{ Path = (Join-Path $workspace 'data'); Dest = (Join-Path $runtimeArchive 'data_20260930') },
    @{ Path = (Join-Path $workspace 'output'); Dest = (Join-Path $runtimeArchive 'output_20260930') },
    @{ Path = (Join-Path $workspace '_rnaseq_benchmark_input'); Dest = (Join-Path $benchmarkArchive '_rnaseq_benchmark_input_20260930') },
    @{ Path = (Join-Path $workspace '0623'); Dest = (Join-Path $historicalArchive '0623_20260930') },
    @{ Path = (Join-Path $workspace 'new_deg3.zip'); Dest = (Join-Path $historicalArchive 'new_deg3.zip') },
    @{ Path = (Join-Path $workspace 'run_agentA_seed.log'); Dest = (Join-Path $historicalArchive 'run_agentA_seed.log') }
)

$records = @()
foreach ($item in $targets) {
    $source = $item.Path
    if (-not (Test-Path -LiteralPath $source)) { continue }
    $resolved = (Resolve-Path -LiteralPath $source).Path
    if (-not ($resolved -eq $workspace -or $resolved.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar))) {
        throw "Refusing outside workspace: $resolved"
    }
    $files = @(Get-ChildItem -LiteralPath $resolved -Recurse -Force -File -ErrorAction SilentlyContinue)
    $bytes = ($files | Measure-Object -Property Length -Sum).Sum
    $records += [PSCustomObject]@{
        original = $resolved
        archived = $item.Dest
        files = $files.Count
        bytes = [int64]$bytes
    }
    if (Test-Path -LiteralPath $item.Dest) { throw "Destination already exists: $($item.Dest)" }
    Move-Item -LiteralPath $resolved -Destination $item.Dest
}

$cacheTargets = @(Get-ChildItem -LiteralPath $workspace -Recurse -Force -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -in @('__pycache__', '.pytest_cache') })
foreach ($cache in $cacheTargets) {
    $resolved = (Resolve-Path -LiteralPath $cache.FullName).Path
    if (-not $resolved.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar)) {
        throw "Refusing outside workspace: $resolved"
    }
    Remove-Item -LiteralPath $resolved -Recurse -Force
}

New-Item -ItemType Directory -Force -Path (Join-Path $workspace 'data'), (Join-Path $workspace 'output') | Out-Null
$manifest = [PSCustomObject]@{
    generated_at = (Get-Date).ToString('s')
    workspace = $workspace
    archived = $records
    removed_caches = $cacheTargets.Count
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $archive 'MANIFEST_20260930.json') -Encoding UTF8
$manifest | ConvertTo-Json -Depth 5

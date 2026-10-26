# Run from repository root. Only lists candidates, never downloads data.
$ErrorActionPreference = "Stop"
Write-Host "Checking common local folders for original UCI transactions..." -ForegroundColor Cyan
$folders = @("$PWD", "$HOME\Downloads", "$HOME\Documents", "D:\porto")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) { continue }
    Get-ChildItem -LiteralPath $folder -File -Recurse -ErrorAction SilentlyContinue |
      Where-Object { $_.Extension -in @('.xlsx', '.csv') -and $_.Name -match 'retail' } |
      Select-Object -ExpandProperty FullName
}
Write-Host "Use the returned FULL file path with --input. Kaggle /kaggle/input paths do not exist on Windows." -ForegroundColor Yellow

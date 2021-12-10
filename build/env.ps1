Write-Host "Setting environment variables...";
$curDir = Get-Location
$Env:CDN_REGISTRY = "localhost:5000"
$Env:CDN_HOME = Split-Path -Path $curDir -Parent
Write-Host "Done";
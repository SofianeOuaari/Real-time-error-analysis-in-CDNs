Write-Host "Setting environment variables...";
$curDir = Get-Location
$Env:CDN_REGISTRY = "localhost:5000"
$Env:CDN_HOME = Split-Path -Path $curDir -Parent
$Env:BURROW_SRC = "D:\OneDrive - Université Nice Sophia Antipolis\M2\Stream Mining\Project\Real-time-error-analysis-in-CDNs\source\Burrow"
Write-Host "Done";
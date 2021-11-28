Write-Host "Setting environment variables...";
$curDir = Get-Location
$Env:CDN_REGISTRY = "localhost:5000"
$Env:CDN_HOME = Split-Path (Split-Path -Path $curDir -Parent) -Parent
Write-Host "Done";

docker-compose build spark
docker-compose push spark
docker-compose pull spark

Write-Host "Complete";
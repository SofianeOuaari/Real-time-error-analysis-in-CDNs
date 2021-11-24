Write-Host "Setting environment variables...";
$curDir = Get-Location
$Env:CDN_REGISTRY = "localhost:5000"
$Env:CDN_HOME = Split-Path -Path $curDir -Parent
Write-Host "Done";
Write-Host "Deploying the docker containers...";

$subfolders = Get-ChildItem -Path ./ -Recurse -Directory -Force -ErrorAction SilentlyContinue | Select-Object FullName 
Foreach ($i in $subfolders)

{
	cd $i.FullName
	docker-compose up -d
}
cd ../
docker run -d --name=grafana -p 3000:3000 grafana/grafana:latest-ubuntu
Write-Host "Complete";
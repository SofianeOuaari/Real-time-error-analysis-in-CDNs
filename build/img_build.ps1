Write-Host "Setting environment variables...";
$curDir = Get-Location
$Env:CDN_REGISTRY = "localhost:5000"
$Env:CDN_HOME = Split-Path -Path $curDir -Parent
$Env:BURROW_SRC = "D:\OneDrive - Université Nice Sophia Antipolis\M2\Stream Mining\Project\Real-time-error-analysis-in-CDNs\source\Burrow"
Write-Host "Done";

docker run -d -p 5000:5000 --restart=always --name registry registry:2

Write-Host "Building the images...";

$subfolders = Get-ChildItem -Path ./ -Recurse -Directory -Force -ErrorAction SilentlyContinue | Select-Object FullName 
Foreach ($i in $subfolders)

{
	$name = Split-Path $i.FullName -Leaf
	cd $i.FullName
	docker-compose build $name
	docker-compose push $name
	docker-compose pull $name
}
cd ../
Write-Host "Complete";
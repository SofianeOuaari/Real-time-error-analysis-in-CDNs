Write-Host "Deleting dangling images...";
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
Write-Host "Complete";
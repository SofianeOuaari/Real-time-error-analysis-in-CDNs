$Env:CDN_REGISTRY = "localhost:5000"
docker run --rm --network host -it $Env:CDN_REGISTRY/cdn_spark:1.0.0 /bin/bash
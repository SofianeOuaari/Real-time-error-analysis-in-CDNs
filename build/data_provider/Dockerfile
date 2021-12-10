ARG CDN_REGISTRY
FROM ${CDN_REGISTRY}/base_python3:1.0.0

WORKDIR /home/cdnadm/

COPY system/ ./system
COPY source/schemas/ ./schemas
COPY source/cdnlib/ ./cdnlib
COPY source/data/test_cdn.csv ./data/
COPY source/data_provider/ .

CMD ["python3", "data_provider.py"]

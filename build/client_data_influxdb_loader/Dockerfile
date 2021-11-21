ARG CDN_REGISTRY
FROM ${CDN_REGISTRY}/base_python3:1.0.0

WORKDIR /home/cdnadm/

COPY system/ ./system
COPY source/cdnlib/ ./cdnlib
COPY source/influxdb_loader/ .

CMD ["python3", "influx_cdn_message_loader.py"]

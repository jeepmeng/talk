#!/bin/bash

# ✅ 定义镜像名称
ES_IMAGE="es-8.13.2-ik"
KIBANA_IMAGE="docker.elastic.co/kibana/kibana:8.13.2"

# ✅ 定义宿主机快照目录
HOST_BACKUP_DIR="/Users/liufucong/Downloads/es_data_new/backup" #本地挂载路径，需要修改

# ✅ 创建备份目录（如果不存在）
mkdir -p "$HOST_BACKUP_DIR"

# ✅ 删除旧容器（如果存在）
docker rm -f es kibana >/dev/null 2>&1

# ✅ 启动 Elasticsearch
docker run -d \
  --name es \
  -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
  -e "path.repo=/mnt/es_backup" \
  -v "$HOST_BACKUP_DIR":/mnt/es_backup \
  "$ES_IMAGE"

# ✅ 启动 Kibana
docker run -d \
  --name kibana \
  --link es \
  -p 5601:5601 \
  -e ELASTICSEARCH_HOSTS=http://es:9200 \
  "$KIBANA_IMAGE"

# ✅ 等待容器就绪并打印状态
echo "✅ 容器启动完成"
echo "📦 Elasticsearch: http://localhost:9200"
echo "📊 Kibana:        http://localhost:5601"
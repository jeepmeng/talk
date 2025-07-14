from encode import encode_vector


from elasticsearch import Elasticsearch
from datetime import datetime
import uuid
import numpy as np  # 或者用你的向量模型

# ✅ 初始化 ES 客户端
es = Elasticsearch("http://localhost:9200")

text = "物模型唯一标识体系："
vec = encode_vector(text)
# ✅ 构造单条文档
doc = {
    "content_uuid": "AyHpCJgBNQ3ihBfHlYpe",                         # 业务关联 ID
    "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 统一格式
    "ques_desc": text,                 # 示例问题描述
    "vector": vec                     # 示例 768 维向量
}

# ✅ 插入到 question_base 索引
res = es.index(index="question_base", body=doc)
print(f"✅ 插入成功，_id = {res['_id']}")
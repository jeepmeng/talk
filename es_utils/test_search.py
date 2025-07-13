from elasticsearch import Elasticsearch
from datetime import datetime
import uuid  # 用于生成唯一 uuid

# ✅ 初始化 ES 客户端
es = Elasticsearch("http://localhost:9200")

# es.search(index="knowledge_base", body={
#     "query": {
#         "match": {
#             "content": "物模型"
#         }
#     }
# })


# doc_id = res["_id"]
# doc = es.get(index="knowledge_base", id='XU0XBJgBPue8yqhl8rOL')
# print(doc)


res = es.search(index="knowledge_base", body={
    "query": {
        "match_all": {}
    },
    "size": 10
})
for hit in res["hits"]["hits"]:
    print(hit["_id"], hit["_source"].get("creat_time"))
    



# es.delete(index="knowledge_base", id="XE0SBJgBPue8yqhlZrMt")
# es.delete(index="knowledge_base", id="XU0XBJgBPue8yqhl8rOL")
# print("✅ 已删除两条异常时间格式文档")

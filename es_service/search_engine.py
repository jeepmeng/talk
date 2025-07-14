# search_engine.py

from elasticsearch import AsyncElasticsearch
from config.settings import settings
from task.gen_vector_chain import encode_text_task
from redis import Redis
import asyncio
import json

# 初始化 ES 客户端 & Redis 客户端
es = AsyncElasticsearch(hosts=[settings.elasticsearch.host])
redis_client = Redis.from_url(settings.vector_service.redis_backend)
INDEX_NAME = settings.elasticsearch.knowledge_base

# BM25 搜索
async def search_bm25(query: str, top_k: int = 10):
    resp = await es.search(
        index=INDEX_NAME,
        size=top_k,
        query={
            "match": {
                "descriptions": {
                    "query": query,
                    "operator": "and"
                }
            }
        }
    )
    return [
        {
            "id": hit["_source"]["uuid"],
            "score": hit["_score"],
            "text": hit["_source"]["descriptions"]
        }
        for hit in resp["hits"]["hits"]
    ]


# 向量搜索（基于 encode_text_task + Redis 获取向量 + ES 向量检索）
async def search_vector(query: str, top_k: int = 10, timeout_sec: int = 5):
    task = encode_text_task.apply_async((query,), kwargs={"use_redis": True})
    redis_key = f"vec_result:{task.id}"

    vec = None
    for _ in range(timeout_sec * 10):
        raw = redis_client.get(redis_key)
        if raw:
            vec = json.loads(raw)
            break
        await asyncio.sleep(0.1)

    if vec is None:
        print(f"❌ 向量获取超时: {query}")
        return []

    resp = await es.search(
        index=INDEX_NAME,
        knn={
            "field": "vector_embeddings",
            "k": top_k,
            "num_candidates": top_k * 10,
            "query_vector": vec
        }
    )
    return [
        {
            "id": hit["_source"]["uuid"],
            "score": hit["_score"],
            "text": hit["_source"]["descriptions"]
        }
        for hit in resp["hits"]["hits"]
    ]


# 融合打分（标准化 + 加权）
def merge_results(bm25_results, vector_results, alpha: float = 0.6):
    def normalize(scores):
        if not scores: return {}
        max_score = max(s["score"] for s in scores) or 1e-5
        return {s["id"]: s["score"] / max_score for s in scores}

    bm25_norm = normalize(bm25_results)
    vector_norm = normalize(vector_results)
    all_ids = set(bm25_norm) | set(vector_norm)

    score_dict = {
        _id: alpha * bm25_norm.get(_id, 0) + (1 - alpha) * vector_norm.get(_id, 0)
        for _id in all_ids
    }

    id_to_text = {
        **{r["id"]: r["text"] for r in bm25_results},
        **{r["id"]: r["text"] for r in vector_results}
    }

    merged = [
        {"id": _id, "score": score_dict[_id], "text": id_to_text[_id]}
        for _id in sorted(score_dict, key=score_dict.get, reverse=True)
    ]
    return merged[:10]
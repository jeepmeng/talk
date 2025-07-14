# search_engine.py
from collections import defaultdict
from elasticsearch import AsyncElasticsearch
from config.settings import settings
from task.gen_vector_chain import encode_text_task
from redis import Redis
import asyncio
import json

# 初始化 ES 客户端 & Redis 客户端
es = AsyncElasticsearch(hosts=[settings.elasticsearch.host])
redis_client = Redis.from_url(settings.vector_service.redis_backend)

KNOWLEDGE_BASE = settings.elasticsearch.knowledge_base
QUESTION_BASE = settings.elasticsearch.question_base

async def search_vector(query: str, top_k: int = 10, timeout_sec: int = 5):
    cache_key = f"vec_cache:{query}"
    vec = None

    # ✅ Step 1: 尝试从 Redis 缓存中拿向量（避免重复 encode）
    raw = redis_client.get(cache_key)
    if raw:
        vec = json.loads(raw)
    else:
        # ✅ Step 2: 没有缓存，发 Celery 异步任务并监听结果
        task = encode_text_task.apply_async((query,), kwargs={"use_redis": True})
        redis_key = f"vec_result:{task.id}"

        for _ in range(timeout_sec * 10):
            raw = redis_client.get(redis_key)
            if raw:
                vec = json.loads(raw)

                # ✅ Step 3: 写入 query-level 缓存，供下次复用
                redis_client.set(cache_key, json.dumps(vec), ex=3600)
                break
            await asyncio.sleep(0.1)

    if vec is None:
        print(f"❌ 向量获取超时: {query}")
        return []

    # 向量搜索（在 QUESTION_BASE 中查 content_uuid）
    vector_resp = await es.search(
        index=QUESTION_BASE,
        knn={
            "field": "vector",
            "k": top_k,
            "num_candidates": top_k * 10,
            "query_vector": vec
        }
    )

    # content_uuid 去重收集
    content_uuids = list({
        hit["_source"]["content_uuid"]
        for hit in vector_resp["hits"]["hits"]
        if "content_uuid" in hit["_source"]
    })

    if not content_uuids:
        return []

    # 根据 content_uuid 反查 KNOWLEDGE_BASE 的原始文本
    kb_resp = await es.mget(
        index=KNOWLEDGE_BASE,
        ids=content_uuids
    )

    uuid_to_content = {
        doc["_id"]: doc["_source"]["content"]
        for doc in kb_resp["docs"]
        if doc["found"]
    }

    # 构造统一结果结构（id: content_uuid, text: content, score: 向量分数）
    return [
        {
            "id": hit["_source"]["content_uuid"],
            "score": hit["_score"],
            "text": uuid_to_content.get(hit["_source"]["content_uuid"], "[未找到原文]")
        }
        for hit in vector_resp["hits"]["hits"]
        if hit["_source"]["content_uuid"] in uuid_to_content
    ]




async def search_bm25(query: str, top_k: int = 10):
    resp = await es.search(
        index=KNOWLEDGE_BASE,
        size=top_k,
        query={
            "match": {
                "content": {
                    "query": query,
                    "operator": "and"
                }
            }
        }
    )

    return [
        {
            "id": hit["_id"],   # content_uuid
            "score": hit["_score"],
            "text": hit["_source"]["content"]
        }
        for hit in resp["hits"]["hits"]
    ]


def merge_results(bm25_results, vector_results, alpha: float = 0.6):
    def normalize(results, epsilon=1e-5):
        if not results: return {}
        scores = [r["score"] for r in results]
        min_s, max_s = min(scores), max(scores)
        if max_s == min_s:
            return {r["id"]: 1.0 for r in results}
        return {
            r["id"]: (r["score"] - min_s + epsilon) / (max_s - min_s + epsilon)
            for r in results
        }

    bm25_results = aggregate_max_by_id(bm25_results)
    vector_results = aggregate_max_by_id(vector_results)

    bm25_norm = normalize(bm25_results)
    vector_norm = normalize(vector_results)
    all_ids = set(bm25_norm) | set(vector_norm)

    # 收集原始文本
    id_to_text = {
        **{r["id"]: r["text"] for r in bm25_results},
        **{r["id"]: r["text"] for r in vector_results}
    }

    merged = []
    for _id in all_ids:
        b_score = bm25_norm.get(_id, 0.0)
        v_score = vector_norm.get(_id, 0.0)
        final_score = alpha * b_score + (1 - alpha) * v_score

        if b_score > 0 and v_score > 0:
            source = "hybrid"
        elif b_score > 0:
            source = "bm25"
        else:
            source = "vector"

        merged.append({
            "id": _id,
            "content": id_to_text.get(_id, ""),
            "score": round(final_score, 4),
            "score_detail": {
                "bm25": round(b_score, 4),
                "vector": round(v_score, 4)
            },
            "source": source
        })

    return sorted(merged, key=lambda x: x["score"], reverse=True)[:10]


def aggregate_max_by_id(results):
    merged = {}
    for r in results:
        if r["id"] not in merged or r["score"] > merged[r["id"]]["score"]:
            merged[r["id"]] = r
    return list(merged.values())
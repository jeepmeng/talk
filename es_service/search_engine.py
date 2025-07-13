# search_engine.py

from elasticsearch import AsyncElasticsearch
from config import settings  # 你自己的配置模块
import aiohttp
import asyncio

# 初始化 ES 客户端
es = AsyncElasticsearch(hosts=[settings.ES_HOST])

# BM25 搜索
async def search_bm25(query: str, top_k: int = 10):
    resp = await es.search(
        index="knowledge_base",
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

# 向量搜索（假设调用向量服务 HTTP 接口）
async def search_vector(query: str, top_k: int = 10):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{settings.VECTOR_SERVICE_URL}/vector-search", json={"query": query, "top_k": top_k}) as resp:
            if resp.status != 200:
                return []
            result = await resp.json()
            return result["results"]  # 假设格式：[{"id": ..., "score": ..., "text": ...}]

# 打分融合函数
def merge_results(bm25_results, vector_results, alpha: float = 0.6):
    score_dict = {}

    # 标准化函数（防止分值相差过大）
    def normalize(scores):
        if not scores: return {}
        max_score = max(s["score"] for s in scores) or 1e-5
        return {s["id"]: s["score"] / max_score for s in scores}

    bm25_norm = normalize(bm25_results)
    vector_norm = normalize(vector_results)

    all_ids = set(bm25_norm) | set(vector_norm)
    for _id in all_ids:
        bm25_score = bm25_norm.get(_id, 0)
        vector_score = vector_norm.get(_id, 0)
        merged_score = alpha * bm25_score + (1 - alpha) * vector_score
        score_dict[_id] = merged_score

    # 获取最终内容（可优化为带缓存）
    id_to_text = {
        **{r["id"]: r["text"] for r in bm25_results},
        **{r["id"]: r["text"] for r in vector_results}
    }

    merged = [
        {"id": _id, "score": score_dict[_id], "text": id_to_text[_id]}
        for _id in sorted(score_dict, key=score_dict.get, reverse=True)
    ]
    return merged[:10]
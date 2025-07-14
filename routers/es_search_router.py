from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from es_service.search_engine import search_bm25, search_vector, merge_results
import asyncio
from routers.schema import (
    # VectorItem,
    # ResponseModel,
    # InsertVectorItem,
    # InsertQuesBatchItem,
    # UpdateByIdItem,
    # FileBatchRequest,
    # WriteQuesBatch,
    SearchRequest,
    SearchResult
)
router = APIRouter()


@router.post("/es_hybrid_search", response_model=List[SearchResult])
async def hybrid_search_api(request: SearchRequest):
    tasks = []
    if request.use_bm25:
        tasks.append(search_bm25(request.query))
    else:
        tasks.append(asyncio.sleep(0, result=[]))

    if request.use_vector:
        tasks.append(search_vector(request.query))
    else:
        tasks.append(asyncio.sleep(0, result=[]))

    bm25_results, vector_results = await asyncio.gather(*tasks)
    print("🎯 vector 原始得分:")
    for r in vector_results:
        print(f"{r['id']} -> {r['score']}")
    merged = merge_results(bm25_results, vector_results, alpha=request.alpha)
    return merged
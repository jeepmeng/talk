from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional
import asyncio
from routers.schema import (
StartDialogRequest,
AskRequest,
ControlRequest
)
from db.dialog_pg import create_session, insert_message, get_history_by_session, get_session_user
from utils.redis_client import get_redis_client
from typing import List
import httpx
from llm_service import call_llm

router = APIRouter()

# Redis 客户端
ioredis = get_redis_client()

@router.post("/dialog/start")
async def start_dialog(data: StartDialogRequest):
    talk_id = uuid4()
    await create_session(talk_id, data.user_id, data.title)
    return {"talk_id": str(talk_id)}

@router.post("/dialog/{talk_id}/ask")
async def ask_question(talk_id: UUID, data: AskRequest):
    # ✅ 检查 talk_id 是否属于 user_id
    session = await get_session_user(talk_id)
    if not session or session.user_id != data.user_id:
        raise HTTPException(status_code=403, detail="无权限访问该对话")

    # ✅ 查询历史对话（优先 Redis）
    redis_key = f"dialog:history:{data.user_id}:{talk_id}"
    history = await ioredis.get(redis_key)
    if history:
        history = eval(history)
    else:
        history = await get_history_by_session(talk_id)
        await ioredis.set(redis_key, str(history), ex=3600)

    # ✅ 调用混合检索
    retrieved = await es_hybrid_search(data.question)

    # ✅ 构造 prompt 调用大模型
    prompt = build_prompt(history, retrieved, data.question)
    response = await call_llm(prompt)

    # ✅ 写入数据库
    await insert_message(talk_id, "user", data.question, None)
    await insert_message(talk_id, "assistant", response, retrieved)

    # ✅ 更新 Redis
    history.append({"role": "user", "content": data.question})
    history.append({"role": "assistant", "content": response})
    await ioredis.set(redis_key, str(history), ex=3600)

    return {"reply": response}

@router.get("/dialog/{talk_id}/history")
async def get_history(talk_id: UUID, user_id: str):
    session = await get_session_user(talk_id)
    if not session or session.user_id != user_id:
        raise HTTPException(status_code=403, detail="无权限访问该对话")

    redis_key = f"dialog:history:{user_id}:{talk_id}"
    history = await ioredis.get(redis_key)
    if history:
        return {"history": eval(history)}
    history = await get_history_by_session(talk_id)
    await ioredis.set(redis_key, str(history), ex=3600)
    return {"history": history}

@router.post("/dialog/{talk_id}/control")
async def control_dialog(talk_id: UUID, data: ControlRequest):
    session = await get_session_user(talk_id)
    if not session or session.user_id != data.user_id:
        raise HTTPException(status_code=403, detail="无权限访问该对话")

    status_key = f"dialog:status:{data.user_id}:{talk_id}"
    await ioredis.set(status_key, data.action)
    return {"status": data.action, "msg": f"对话已设置为 {data.action}"}


def build_prompt(history: List[dict], retrieved: List[str], user_input: str):
    prompt = ""
    for h in history[-5:]:
        prompt += f"{h['role']}: {h['content']}\n"
    if retrieved:
        prompt += "\n以下是知识库中可能相关的信息：\n"
        for i, r in enumerate(retrieved):
            prompt += f"[信息{i+1}] {r}\n"
    prompt += f"\nuser: {user_input}\nassistant:"
    return prompt


async def es_hybrid_search(question: str) -> List[str]:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            "http://localhost:8001/es_hybrid_search",
            json={"query": question}
        )
        response.raise_for_status()
        return [r["content"] for r in response.json()]
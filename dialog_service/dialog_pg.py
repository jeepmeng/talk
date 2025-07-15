from uuid import UUID
from typing import Optional, List
from db_service.pg_pool import pg_conn  # ✅ 使用你已有的连接管理器

# ✅ 创建对话会话
async def create_session(talk_id: UUID, user_id: str, title: Optional[str] = None):
    async with pg_conn() as conn:
        await conn.execute(
            """
            INSERT INTO dialog_sessions (talk_id, user_id, title, created_at)
            VALUES ($1, $2, $3, NOW())
            """,
            talk_id, user_id, title
        )

# ✅ 插入对话消息
async def insert_message(talk_id: UUID, role: str, content: str, vector_result: Optional[List[dict]] = None):
    async with pg_conn() as conn:
        await conn.execute(
            """
            INSERT INTO dialog_messages (id, talk_id, role, content, vector_search_result, created_at)
            VALUES (gen_random_uuid(), $1, $2, $3, $4, NOW())
            """,
            talk_id, role, content, vector_result
        )

# ✅ 查询对话历史
async def get_history_by_session(talk_id: UUID) -> List[dict]:
    async with pg_conn() as conn:
        rows = await conn.fetch(
            """
            SELECT role, content
            FROM dialog_messages
            WHERE talk_id = $1
            ORDER BY created_at ASC
            """,
            talk_id
        )
        return [dict(row) for row in rows]

# ✅ 查询该 talk_id 所属的 user_id
async def get_session_user(talk_id: UUID):
    async with pg_conn() as conn:
        row = await conn.fetchrow(
            """
            SELECT talk_id, user_id, title
            FROM dialog_sessions
            WHERE talk_id = $1
            """,
            talk_id
        )
        return dict(row) if row else None
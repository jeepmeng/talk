from typing import Optional, List, Dict, Any
from pydantic import BaseModel,HttpUrl
from uuid import UUID, uuid4

# ✅ 请求数据模型
class VectorItem(BaseModel):
    id: Optional[str] = None
    text: str


class ResponseModel(BaseModel):
    msg: str
    data: Optional[dict] = None


# 插入向量记录
class InsertVectorItem(BaseModel):
    zhisk_file_id: int
    content: str
    vector: List[float]
    jsons: Dict[str, Any]
    code: str
    category: str
    uu_id: str


# 批量插入问题
class InsertQuesBatchItem(BaseModel):
    uu_id: str
    sentences: List[str]
    vectors: List[List[float]]


# 更新记录字段
class UpdateByIdItem(BaseModel):
    update_data: Dict[str, Any]
    record_id: int
    updata_ques: List[str]
    up_ques_vect: List[List[float]]



class FileMeta(BaseModel):
    url: str
    filename: str
    file_id: str

class FileBatchRequest(BaseModel):
    files: List[FileMeta]






class WriteQuesBatch(BaseModel):
    uu_id: str
    sentences: list[str]
    vectors: list[list[float]]


class SearchRequest(BaseModel):
    query: str
    use_bm25: bool = True
    use_vector: bool = True
    alpha: float = 0.6  # 权重

# class SearchResult(BaseModel):
#     id: str
#     text: str
#     score: float



class ScoreDetail(BaseModel):
    bm25: float
    vector: float

class SearchResult(BaseModel):
    id: str
    content: str
    score: float
    score_detail: Dict[str, float]
    source: str  # "hybrid", "bm25", "vector"



class StartDialogRequest(BaseModel):
    user_id: str
    title: Optional[str] = None

class AskRequest(BaseModel):
    user_id: str
    question: str

class ControlRequest(BaseModel):
    user_id: str
    action: str  # stop | pause | resume | resend
    message_id: Optional[UUID] = None


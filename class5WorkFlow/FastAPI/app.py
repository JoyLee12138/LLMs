from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
import torch

# ---------------------------
# 1. FastAPI 实例
# ---------------------------
app = FastAPI(title="RAG FastAPI Demo")

# ---------------------------
# 2. 请求体定义
# ---------------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

# ---------------------------
# 3. 加载 reranker 模型
# ---------------------------
# 这里用 bge-reranker-large
reranker_model_name = "BAAI/bge-reranker-large"
reranker_model = SentenceTransformer(reranker_model_name, device="cpu")

# ---------------------------
# 4. 模拟文档库
# ---------------------------
# 实际可以换成 Chroma / Milvus / 本地 RAG 文档
documents = [
    "FastAPI 是一个 Python Web 框架。",
    "RAG 可以把检索的文档拼接进 prompt。",
    "Embedding 是向量化文本的方法。",
    "Python 可以用来做 AI 模型服务。",
    "bge-reranker-large 是一个向量 rerank 模型。"
]

# ---------------------------
# 5. 简单检索 + rerank 函数
# ---------------------------
def simple_rerank(query: str, top_k: int = 5):
    # query embedding
    query_emb = reranker_model.encode([query], normalize_embeddings=True)
    
    # 文档 embedding
    doc_embs = reranker_model.encode(documents, normalize_embeddings=True)
    
    # 计算相似度
    scores = (torch.tensor(query_emb) @ torch.tensor(doc_embs).T).squeeze(0)
    
    # top_k 排序
    topk_idx = torch.topk(scores, k=min(top_k, len(documents))).indices.tolist()
    
    # 返回结果
    top_docs = [{"doc": documents[i], "score": float(scores[i])} for i in topk_idx]
    return top_docs

# ---------------------------
# 6. 定义 FastAPI 接口
# ---------------------------
@app.post("/query")
def query_endpoint(request: QueryRequest):
    top_docs = simple_rerank(request.query, request.top_k)
    return {"query": request.query, "top_docs": top_docs}


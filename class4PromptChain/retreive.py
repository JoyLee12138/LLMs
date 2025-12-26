# retrieve.py
from typing import List, Dict
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb
import os
HF_TOKEN = os.getenv("hf_")

# 全局加载模型（只加载一次）
EMBED_MODEL = SentenceTransformer("BAAI/bge-small-zh-v1.5", device="cpu")
RERANK_MODEL = CrossEncoder("BAAI/bge-reranker-base", device="cpu")


def retrieve_top_k(
    collection,
    query: str,
    embed_model,
    top_k: int = 15
):
    query_embedding = embed_model.encode(query, normalize_embeddings=True).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results


def rerank_results(
    query: str,
    candidates: List[Dict],
    rerank_model,
    top_n: int = 5
):
    # 构造 (query, passage) 对
    pairs = [(query, c["text"]) for c in candidates]
    scores = rerank_model.predict(pairs)

    # 按分数降序排序
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

    # 返回结构化结果（注意：用 metadata 单数）
    return [
        {
            "id": c["id"],
            "text": c["text"],
            "metadata": c["metadata"],          # ← 改为单数 metadata
            "rerank_score": float(score)
        }
        for c, score in ranked[:top_n]
    ]


def retrieve(collection, query: str, top_k: int = 15, top_n: int = 5):
    # 使用全局模型，避免重复加载
    raw = retrieve_top_k(collection, query, EMBED_MODEL, top_k=top_k)

    ids = raw["ids"][0]
    docs = raw["documents"][0]
    metadatas = raw["metadatas"][0] if raw["metadatas"] and raw["metadatas"][0] else [{}] * len(ids)

    # 构建 candidates，统一用 "metadata"（单数）
    candidates = [
        {"id": id_, "text": doc, "metadata": meta}
        for id_, doc, meta in zip(ids, docs, metadatas)
    ]

    return rerank_results(query, candidates, RERANK_MODEL, top_n=top_n)



if __name__ == "__main__":
    # 假设你已有 collection（可从 ingest 中获取）
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="tldr_demo")

    query = "pkg的install相关指令有哪些？"
    results = retrieve(collection, query, top_k=15, top_n=5)

    for i, res in enumerate(results, 1):
        print(f"\n[{i}] Score: {res['rerank_score']:.4f}")
        print(f"Source: {res['metadata'].get('source', 'N/A')}")
        print(f"Text: {res['text'][:500]}...")
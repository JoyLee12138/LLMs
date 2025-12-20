
from openai import OpenAI
import chromadb
from chromadb.config import Settings
import mychromadb
import LLMrerank
from embedding import embed_texts


def rag_with_rerank(collection, query):
    # 1. embedding 召回
    candidates = LLMrerank.retrieve_candidates(collection, query, top_k=15)

    # 2. rerank
    reranked = LLMrerank.rerank_with_llm(query, candidates)

    # 3. 取 top_n
    final_docs = [doc for _, doc in reranked[:5]]

    return final_docs


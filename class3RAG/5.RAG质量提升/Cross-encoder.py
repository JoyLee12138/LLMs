from openai import OpenAI
import chromadb
from chromadb.config import Settings
import mychromadb

from embedding import embed_texts

from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_with_ce(query, docs):
    pairs = [(query, doc) for doc in docs]
    scores = reranker.predict(pairs)

    scored_docs = list(zip(scores, docs))
    scored_docs.sort(reverse=True)
    return scored_docs

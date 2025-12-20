from openai import OpenAI
import chromadb
from chromadb.config import Settings
import mychromadb

from embedding import embed_texts
RERANK_PROMPT = """
你是一个严谨的问答助手。
请严格根据【资料】回答【问题】。
如果【资料】中没有相关信息，请回答：“我不知道”。

【资料】
{doc}

【问题】
{query}

【回答】
"""





client = chromadb.Client(Settings(persist_directory = r"D:\Code\ML\LLMs\class3RAG\5.RAG质量提升\mychroma_db"))
collection = client.get_collection("demo")
# collection = client.get_or_create_collection("demo")
print("Starting query.py")





query="接口怎么定义的?"
query_embedding = embed_texts([query])[0]


#topk=15
def retrieve_candidates(collection, query, top_k=15):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    docs = results["documents"][0]
    return docs




#用模型rerank返回分数
def rerank_with_llm(query, docs):
    scored_docs = []

    for doc in docs:
        prompt = RERANK_PROMPT.format(
            query=query,
            doc=doc
        )

        resp = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        try:
            score = float(resp.choices[0].message.content.strip())
        except:
            score = 0.0

        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return scored_docs


import numpy as np
from sentence_transformers import SentenceTransformer

# 1. 强制 CPU
model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5",
    device="cpu"
)

documents = [
    "大模型可以用于文本生成和问答",
    "语言模型能够回答问题并生成自然语言",
    "深度学习模型常用于图像识别",
    "今天东京的天气非常好",
    "我喜欢吃拉面"
]

def get_embedding(text):
    return model.encode(text, normalize_embeddings=True)

# 2. 文档 embedding 一次性算好
doc_embeddings = [get_embedding(d) for d in documents]

def cosine_similarity(a, b):
    return np.dot(a, b)

def search(query, top_k=3):
    query_emb = get_embedding(query)
    scores = []

    for doc, emb in zip(documents, doc_embeddings):
        score = cosine_similarity(query_emb, emb)
        scores.append((doc, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

# 3. 测试
queries = [
    "大语言模型能做什么？",
    "你喜欢吃什么？"
]

for q in queries:
    print(f"\nQuery: {q}")
    for doc, score in search(q):
        print(f"{score:.4f} | {doc}")

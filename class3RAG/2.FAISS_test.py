import faiss
import numpy as np

dim = 3
vectors = np.array([
    [1, 0, 0],
    [0.9, 0.1, 0],
    [0, 1, 0],
    [0, 0, 1],
]).astype("float32")

index = faiss.IndexFlatL2(dim)
index.add(vectors)

query = np.array([[1, 0, 0]]).astype("float32")
D, I = index.search(query, k=2)

print(I)  # 返回最相似向量的索引
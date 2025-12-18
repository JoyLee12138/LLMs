import chromadb
from chromadb.config import Settings
from embedding import embed_texts
from chunking import chunk_text

#读文档
with open('simple.txt', 'r',encoding='utf-8') as f:
  documents = f.read()

#chunk文档
chunks = chunk_text(documents)
print("chunks个数为：",len(chunks))

#embed文档
embeddings = embed_texts(chunks)
print("embeddings结束！")

#初始化chroma数据库
client = chromadb.Client(Settings(persist_directory = r"D:\Code\ML\LLMs\class3RAG\ragdemo\mychroma_db"))
collection = client.create_collection("demo")
collection.add(documents=chunks, embeddings=embeddings,metadatas=[{"source": "simple.txt", "chunk": i} for i in range(len(chunks))],ids=[f"chunk{i}" for i in range(len(chunks))])

print(collection.count())

print("chroma数据库初始化完成！")

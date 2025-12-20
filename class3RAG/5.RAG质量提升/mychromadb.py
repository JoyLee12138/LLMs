import chromadb
from chromadb.config import Settings
from embedding import embed_texts
import chunking

#读文档
with open('文档.md', 'r',encoding='utf-8') as f:
  documents = f.read()

#chunk文档
chunks = chunking.recursive_chunk(documents)
print("fixed_chunk的chunks个数为：",len(chunks))

# chunks = chunking.recursive_chunk(documents)
# print("recursive_chunk的chunks个数为：",len(chunks))

# chunks = chunking.semantic_chunk_md(documents)
# print("semantic_chunk_md的chunks个数为：",len(chunks))



#embed文档
embeddings = embed_texts(chunks)
print("embeddings结束！")

#初始化chroma数据库
client = chromadb.Client(Settings(persist_directory = r"D:\Code\ML\LLMs\class3RAG\5.RAG质量提升\mychroma_db"))
collection = client.create_collection("demo")
collection.add(documents=chunks, embeddings=embeddings,metadatas=[{"source": "文档.txt", "chunk": i} for i in range(len(chunks))],ids=[f"chunk{i}" for i in range(len(chunks))])

print(collection.count())

print("chroma数据库初始化完成！")

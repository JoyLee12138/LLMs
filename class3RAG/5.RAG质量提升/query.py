import chromadb
import mychromadb
from chromadb.config import Settings
from embedding import embed_texts

client = chromadb.Client(Settings(persist_directory = r"D:\Code\ML\LLMs\class3RAG\5.RAG质量提升\mychroma_db"))
collection = client.get_collection("demo")
# collection = client.get_or_create_collection("demo")
print("Starting query.py")





query="接口怎么定义的?"
query_embedding = embed_texts([query])[0]


result = collection.query(
  query_embeddings=[query_embedding],
  n_results=3
)

for doc,meta,dist in zip(
  result["documents"][0],
  result["metadatas"][0],
  result["distances"][0]):
  print("分割线-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------分割线")
  print(meta)
  print("dist:",dist)
  print(doc)
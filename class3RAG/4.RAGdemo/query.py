import chromadb
import mychromadb
from chromadb.config import Settings
from embedding import embed_texts

# client = chromadb.Client(Settings(persist_directory = r"D:\Code\ML\LLMs\class3RAG\ragdemo\mychroma_db"))
# collection = client.get_collection("demo")
# # collection = client.get_or_create_collection("demo")



def query(query, k=3):
  client = chromadb.Client(Settings(
  persist_directory=r"D:\Code\ML\LLMs\class3RAG\ragdemo\mychroma_db"
))

  collection = client.get_collection("demo")
  query_embedding = embed_texts([query])[0]
  result = collection.query(
    query_embeddings=[query_embedding],
    n_results=k
  )
  return result["documents"][0]
# query="what is Augmented Generation (RAG)?"
# query_embedding = embed_texts([query])[0]


# result = collection.query(
#   query_embeddings=[query_embedding],
#   n_results=3
# )

# for doc,meta,dist in zip(
#   result["documents"][0],
#   result["metadatas"][0],
#   result["distances"][0]):
#   print("-------------------------")
#   print(meta)
#   print("dist:",dist)
#   print(doc)
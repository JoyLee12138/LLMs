import chromadb
from chromadb.config import Settings
client = chromadb.Client(Settings(persist_directory = "./chroma_test"))
collection = client.create_collection("demo")

documents=["vector about machine learning",
           "deep learning and neural networks",
           "today is Sunday",
           "stock market is up"]

embeddings = [
  [1,0,0],
  [0.9,0.1,0],
  [0,1,0],
  [0,0,1],
]
metadatas= [{"topic":"ai"},
            {"topic":"ai"},
            {"topic":"weather"},
            {"topic":"finance"}]
ids = ["doc1","doc2","doc3","doc4"]

collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas,ids=ids)

query_embedding = [1,0,0]

result = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)
print(result["ids"])
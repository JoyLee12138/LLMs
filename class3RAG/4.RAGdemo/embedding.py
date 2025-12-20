from openai import OpenAI
from sentence_transformers import SentenceTransformer
# from dotenv import load_dotenv, find_dotenv

# _=load_dotenv(find_dotenv())  # 读取 .env 文件中的环境变量
# client = OpenAI(api_key="")
# def embed_texts(texts):
#   response = client.embeddings.create(
#     model="text-embedding-ada-002",
#     input=texts
#   )
#   return [item.embedding for item in response.data]
model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5",
    device="cpu"
)

def embed_texts(texts):
    return model.encode(texts, normalize_embeddings=True).tolist()
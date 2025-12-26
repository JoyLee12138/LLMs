#文档->chunks->embeddings->DB
import re
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

#Embedding
def load_embedding_model():
    return SentenceTransformer(
        "BAAI/bge-small-zh-v1.5",
        device="cpu"
    )

def embed_texts(model,texts):
    return model.encode(texts,normalize_embeddings=True).tolist()


#Chunk--递归切分
#(?<=[。.!?]) 是一个零宽正向后瞻断言（positive look-behind）：匹配位于句号 。、句点 .、问号 ？、感叹号 ！ 之后的那个“缝隙”；只认这些标点，但不把标点本身吃掉，所以切完后标点仍保留在句尾。
# def chunk_text(text, max_length=500):
#     chunks = []
#     paragraphs = text.split("\n\n")

#     for p in paragraphs:
#         if len(p) <= max_length:
#             chunks.append(p)
#         else:
#             sentences=re.split(r'(?<=[。.!?])', p)
#             buf=""
#             for s in sentences:
#                 if len(buf)+len(s)<=max_length:
#                     buf += s
#                 else:
#                     chunks.append(buf)
#                     buf = s
#             if buf:
#                 chunks.append(buf)
#     return chunks
#滑动窗口
# def chunk_text(text, max_length=500, overlap=50):
#     if not text:
#         return []
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + max_length
#         chunks.append(text[start:end])
#         start = end - overlap if end - overlap < len(text) else len(text)
#         if start >= len(text):
#             break
#     return chunks

#固定长度chunking
def chunk_text(text, max_length=500):
    chunks = []
    start = 0
    print("输出chunk的块")
    while start < len(text):
        end = start + max_length
        # print(text[start:end])
        # print("*****************")
        chunks.append(text[start:end])
        start = end - 50
    return chunks

#向量库
def build_chroma_index_from_dir(
        docs_dir:str,

        persist_dir:str,
        chunk_size:int=500,
        max_length:int=500,
        collection_name:str="demo"):
    model = load_embedding_model()
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name=collection_name)
    docs_id = 0
    for path in Path(docs_dir).rglob("*.md"):
        # print("==========================================")
        # print(path)
        with open(path,"r",encoding="utf-8") as f:
            text = f.read()
            chunks = chunk_text(text,max_length=max_length)
            embeddings = embed_texts(model,chunks)
            collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas = [{"source": str(path), "chunk_id": i}for i in range(len(chunks))],
                ids=[f"{path.stem}_{docs_id}_{i}" for i in range(len(chunks))]
            )
            docs_id += 1
            print(f"已处理：{path} | chunks={len(chunks)}")
    print(f"collection 文档数：{collection.count()}")
    print("Chroma 数据库初始化完成")
    return collection




#CLI
if __name__ == "__main__":
    build_chroma_index_from_dir(
        docs_dir="./tldr-main/pages/android",
        persist_dir="./chroma_db",
        collection_name="tldr_demo"
    )

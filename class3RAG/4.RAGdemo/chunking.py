#做文档分割
#整个流程：chunking->embedding->向量搜索匹配(FAISS)->Prompt生成
def chunk_text(text, chunk_size=300,overlap=50):
  chunks = []
  start =0
  while start < len(text):
    end = min(start+chunk_size,len(text))
    chunk = text[start:end]
    chunks.append(chunk)
    start += (chunk_size-overlap)
  return chunks
import chromadb
from chromadb.config import Settings
from embedding import embed_texts
from chunking import chunk_text
import query
import mychromadb
from openai import OpenAI

#初始化LLM
llm = OpenAI(api_key="sk你的key")
question = "what is Augmented Generation (RAG)?"
chunks = query.query(question,3)
#构建context
context = "\n\n".join(chunks)
prompt = f"""你是一个严谨的问答助手。
请严格根据【资料】回答【问题】。
如果【资料】中没有相关信息，请回答：“我不知道”。

【资料】
{context}

【问题】
{question}

【回答】
"""
response = llm.chat.completions.create(
  model="gpt-4o-mini",
  messages=[{"role": "user", "content": prompt}],
  temperature=0)


answer = response.choices[0].message.content
print("answer:",answer)
#prompt 模板（先是单步）
from typing import List, Dict


#构建上下文
def build_context(chunks:List[Dict]):
  lines=[]
  for c in chunks:
    meta=c.get("metadata",{})
    chunk_id = meta.get("chunk_id","N/A")

    lines.append(f"[Chunk {chunk_id}]\n {c['text']}")
  return "\n\n".join(lines)
  
#v1 RAG Prompt：提取信息，总结摘要
def first_step_prompt(context:str,query:str):
  return f"""你是一个严谨、保守的问答助手。
请严格根据【资料】，抽取关键信息，生成摘要。
不允许使用常识或资料以外的信息。

【资料】
{context}

【问题】
{query}

请给出准确、简洁 的回答。如果资料中没有相关信息，请明确回答：“根据提供的文档，我无法回答这个问题。”
""".strip()


def last_step_prompt(summary:str,query:str):
  return f"""你是一个严谨、保守的问答助手。
请严格根据【摘要】，回答问题。
不允许使用常识或资料以外的信息。

【摘要】
{summary}

【问题】
{query}

请给出准确、简洁 的回答。如果摘要中没有相关信息，请明确回答：“根据提供的文档，我无法回答这个问题。”
""".strip()
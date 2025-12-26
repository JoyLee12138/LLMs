# retrieve->prompt->LLM->answer
import chromadb
from chromadb import PersistentClient
import retreive
import ingest
import build_prompt
import dashscope
from dashscope import Generation

#初始化LLM
# 设置你的 API Key（替换成你自己的）
dashscope.api_key = "sk-a06bcd19213642c88de201d0941a286a"

# 调用 Qwen 模型




def call_llm(prompt: str) -> str:

    rsp = dashscope.Generation.call(
        model="qwen-max",
        prompt=prompt,
        temperature=0
    )
    # 千问把答案放在 rsp.output["text"]
    if rsp.status_code == 200 and rsp.output:
        return rsp.output["text"]
    else:
        raise RuntimeError(f"千问调用失败：{rsp.code} {rsp.message}")

#初始化向量库
def load_collection(
    persist_directory: str,
    collection_name: str
):
    client = PersistentClient(path=persist_directory)
    collection = client.get_or_create_collection(name=collection_name)
    return collection


#主查询流程
def run_query(
      query:str,
      persist_directory:str= "./chroma_db",
      collection_name: str="tldr_demo",
      top_k=15,
      top_n=5
):
   #1.加载向量库
   collection=load_collection(persist_directory,collection_name)
   count=collection.count()
   print("库内文档数：", count)
   #2，检索+rerank
   retrieve_chunks=retreive.retrieve(collection,query,top_k,top_n)
   print("检索到文档数：", len(retrieve_chunks))
   # print("检索到文档：", retrieve_chunks)
   #3，prompt
   context=build_prompt.build_context(retrieve_chunks)
   # print("==========================================")
   # print("上下文：", context)
   print("==========================================")
   summary_prompt = build_prompt.first_step_prompt(context,query)
   summary = call_llm(summary_prompt)
   print(summary)
   prompt = build_prompt.last_step_prompt(summary,query)
   #4，LLM
   answer=call_llm(prompt)
   return answer


#CLI
if __name__ == "__main__":
    user_query = "pkg的install相关指令有哪些？"
    answer = run_query(user_query)
    print(answer)
import os
import sys
from huggingface_hub import InferenceClient
#角色-任务-格式-例子四要素
hf=os.getenv("HF_TOKEN") or sys.exit("请设置 HF_TOKEN 环境变量 (hf_xxx)")
c=InferenceClient(api_key=hf)

def ask(text): return c.chat.completions.create(model="Qwen/Qwen3-VL-8B-Instruct:novita", messages=[{"role":"user","content":[{"type":"text","text":text}]}]).choices[0].message["content"]

def summarize(t): return ask(f"请用一句话总结：{t}")

def translate(t,lang="English"): return ask(f"请将以下文本翻译成{lang}：{t}")

if __name__=="__main__":
    q=input("问题: ");print("回答:",ask(q));t=input("待摘要/翻译文本: ");print("摘要:",summarize(t));print("翻译:",translate(t))
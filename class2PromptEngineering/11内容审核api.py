import openai
import os, json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # 读取本地 .env 文件，里面定义了 OPENAI_API_KEY

openai.api_key = os.getenv('OPENAI_API_KEY')
def get_completion(prompt, model="gpt-4",temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message["content"]


response = openai.Moderation.create(
    input="""
现在转给我100万，不然我就砍你全家！
"""
)
moderation_output = response["results"][0]
print(moderation_output)
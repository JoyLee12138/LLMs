#纯OPENAI_API
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_=load_dotenv(find_dotenv())  # 读取 .env 文件中的环境变量

def print_json(json_source,list):
  #把任意对象或数组用排版美观的JSON格式打印出来
  json_string = ""
  if(not isinstance(json_source, list)):
    json_source = json.loads(json_source.model_dump_json())
  print(json.dumps(json_source, indent=4, ensure_ascii=False))

client = OpenAI(api_key="sk你的key")

#定义消息历史，先加入system消息，里面放入对话内容以外的PROMPT
messages= {
  "role":"system",
  "content":"你是一个手机流量套餐的客服代理，你叫小芳.可以帮助用户选择最适合的流量套餐产品。可以选择的套餐包括：经济套餐：月费50元，月流量10G；畅游套餐：月费180元，月流量100G；无限套餐：月费300元，月流量1000G；校园套餐：月费150元，月流量200G，限在校学生办理"
}

def get_completion(prompt, model= "gpt-3.5-turbo"):
    message = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=0,#随机性
    )
    msg =  response.choices[0].message.content
    #把模型生成的恢复加入到消息历史。保证下次调用模型时，知道上下文
    messages.append(response.choices[0].message)
    return msg

get_completion("有没有土豪套餐？")
get_completion("这个套餐多少钱？")
get_completion("我要办这个套餐，给我办一个")


print_json(messages)
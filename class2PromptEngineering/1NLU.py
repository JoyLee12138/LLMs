from openai import OpenAI
#.env 是存放环境变量（例如 API 密钥、配置项）的小文件格式；dotenv 是一类工具/库，用来从这个文件把环境变量加载到运行时环境，方便本地开发且避免把敏感信息写入源码。
from dotenv import load_dotenv, find_dotenv

_=load_dotenv(find_dotenv())  # 读取 .env 文件中的环境变量
client = OpenAI(api_key="sk你的key")  # 初始化 OpenAI 客户端实例

def get_completion(prompt, model= "gpt-3.5-turbo"):
    message = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=0,#随机性
    )
    return response.choices[0].message.content


#实现一个NLU
#任务描述
instruction = """你的任务是识别用户对手机流量套餐产品的选择条件。每种流量套餐产品包含三个属性：名称，月费价格，月流量。根据用户输入，识别用户在上述三种属性上的倾向。"""
#用户输入
input_text = """办一个100G的套餐。"""
#prompt 模板。instruction和input_text会被替换为上面的内容
prompt = f"""{instruction}
用户输入: {input_text}"""




#1.
#调用大模型
response = get_completion(prompt)
print(response)



#2.
#约定输出格式
output_format = """以JSON格式输出"""
prompt = f"""{instruction}
{output_format}
用户输入: {input_text}"""
response = get_completion(prompt)
print(response)



#3.
#把输出格式定义的更精细
output_format = """以JSON格式输出，包含以下字段：
- price_preference: 用户对月费价格的倾向，取值可以是 "low"（低），"medium"（中），"high"（高），或者 "no_preference"（无偏好）。
- data_preference: 用户对月流量的倾向，取值可以是 "low"（低），"medium"（中），"high"（高），或者 "no_preference"（无偏好）。
- additional_requirements: 用户的其他要求，字符串类型，如果没有则为 "none"。"""
prompt = f"""{instruction}
{output_format}
用户输入: {input_text}"""
response = get_completion(prompt)   
print(response)

#4.加入例子
example = """示例：
便宜的套餐：{"sort":{"ordering"="ascend","value"="price"}}
不限流量的套餐：{"data":{"operator":"==","value"="无上限"}}"""

input_text = """有没有便宜的套餐"""
prompt = f"""{instruction}
{output_format}
例如：  {example}
用户输入: {input_text}"""
response = get_completion(prompt)
print(response)
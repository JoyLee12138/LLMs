import openai
import os, json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # 读取本地 .env 文件，里面定义了 OPENAI_API_KEY

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_chat_completion(session, user_prompt, model="gpt-3.5-turbo"):
    _session = copy.deepcopy(session)
    _session.append({"role": "user", "content": user_prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=_session,
        temperature=0,  # 生成结果的多样性 0~2之间，越大越随机，越小越固定
        seed=None,#随机数种子，指定具体值后，temperature为0时，每次生成的结果都是一样的
        top_p=1,#随机采样时，只考虑概率前10%的token，不建议和temperature一起用
        n=1,  # 一次生成n条结果
        max_tokens=100,  # 每条结果最多多少个token（超过截断）
        presence_penalty=0,  # 对出现过的token的概率进行降权
        frequency_penalty=0,  # 对出现过的token根据其出现过的频次，对其的概率进行降权
        stream=False, #数据流模式，一个个字接收
        logit_bias=None, #对token的采样概率手工加/降权，不常用  
        # top_p = 0.1, #随机采样时，只考虑概率前10%的token，不常用
    )
    system_response = response.choices[0].message["content"]
    #session.append({"role": "assistant", "content": system_response})
    return system_response
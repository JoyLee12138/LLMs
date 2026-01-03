def search(query:str) -> str:
    return f"搜索结果：这是关于'{query}'的搜索结果。"

def calculator(expression: str) -> str:
    try:
        return str(eval(expression))#把字符串当成表达式来计算
    except Exception as e:
        return f"计算错误: {e}"


#finih本身不是工具，本质是停止信号
def finish(answer: str) -> str:
    return f"最终答案是: {answer}"



Tools = {
    "search": search,
    "calculator": calculator,
    "finish": finish
}


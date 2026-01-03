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


def retrieve(query: str) -> str:
    """
    从你的知识库中检索相关文档
    """
    # 这里先 mock，下一步你换成真实 RAG
    return (
        "【文档1】Transformer 是一种由 Vaswani 等人在 2017 年提出的深度学习架构。\n"
        "【文档2】Transformer 使用自注意力机制，摒弃了传统的 RNN 和 CNN。"
    )

Tools = {
    "search": search,
    "calculator": calculator,
    "finish": finish,
    "retrieve": retrieve,
    }


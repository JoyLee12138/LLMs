import json
from typing import List, Dict, Any,Callable
#1.Tool定义
def search_docs(query: str) -> str:
    # retrieve 
    return f"模拟检索结果与'{query}'相关的文档内容"

TOOLS:Dict[str, Callable] = {"search_docs": search_docs}


#2.ReAct Agent Prompt模板
PROMPT_TEMPLATE = """你是一个智能助理，可以使用工具来回答问题。
你可以使用以下工具：
{tool_desc}


请严格按照以下格式回复：
Thought:你的思考
Action:{{"name": "工具名称", "args": {{...}}  }}

或

Final:最终答案




用户问题：{query}


历史记录：{scratchpad}

""" 

#3.LLM Stub
def call_llm(prompt: str) -> str:
    #先写死，后面换成我自己的LLM
    return"""
Thought:我需要检索相关文档来回答这个问题。
Action:{"name": "search_docs", "args": {"query": "示例问题"}}
"""


#4.Agent主循环体
def null_agent(query: str,max_steps=5) -> str:
    state={
        "query": query,
        "scratchpad": [],
    }
    for step in range(max_steps):
        #构建prompt
        prompt = PROMPT_TEMPLATE.format(
            tool_desc=TOOLS.keys(),
            query=state["query"],
            scratchpad=state["scratchpad"]
        )
        #调用LLM
        llm_output = call_llm(prompt)


        #解析LLM输出
        #Final
        if "Final:" in llm_output:
            final_answer = llm_output.split("Final:")[-1].strip()
            return final_answer
        
        #Parse Action
        try:
            action_str = llm_output.split("Action:")[-1].strip()
            action = json.loads(action_str)
            tool_name = action["name"]
            tool_args = action["args"]
        except Exception as e:
            raise ValueError(f"无法解析LLM输出: {llm_output}") from e
        
        #Calling Tool
        if tool_name not in TOOLS:
            raise ValueError(f"未知工具: {tool_name}")
        observation = TOOLS[tool_name](**tool_args)


        #Scratchpad更新
        state["scratchpad"].append({"thought": llm_output})

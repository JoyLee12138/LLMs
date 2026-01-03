import re
from tools import Tools
from llm import call_llm
from prompt import REACT_PROMPT


#限制retrive调用次数
MAX_RETRIEVE = 1
retrieve_count = 0
#限制agent最大步数
MAX_STEPS = 5


def parse_action(text: str):
    try:
        action = re.search(r"Action:\s*([a-zA-Z_]+)", text)
        action_input = re.search(r"Action Input:\s*([\s\S]+)", text)

        if not action or not action_input:
            return None, None

        return action.group(1).strip(), action_input.group(1).strip()
    except Exception:
        return None, None

def run_agent(question:str):
    history = ""
    for step in range(MAX_STEPS):
        prompt = REACT_PROMPT.format(question=question, history=history)
        response = call_llm(prompt)
        print(f"\n===Step {step}===")
        print(response)

        action, action_input = parse_action(response)
        if action is None:
          print("⚠️ 解析失败，模型输出不符合 ReAct 格式")
          print(response)
          return "❌ Agent 解析失败"
        if action not in Tools:
            print("无法解析动作，结束。")
            return "无法解析  动作，结束。"
        result= Tools[action](action_input.strip())

        # 限制 retrieve 调用次数，防止agent发疯一直retrieve
        if action == "retrieve":
            if retrieve_count >= MAX_RETRIEVE:
                history += "\nObservation: 【已达到最大检索次数】"
                continue
            retrieve_count += 1

        if action == "finish":
            print("最终答案：", result)
            return result
        history += f"\n{response}\nObservation: {result}"
    print("达到最大步骤数，结束。")
    return "达到最大步骤数，结束。"

if __name__ == "__main__":
    answer = run_agent("什么是Transformer？")
    print("Agent的回答：", answer)
       
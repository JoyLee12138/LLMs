import json
from typing import List, Dict, Any,Callable
def prompt_agent(query: str, tool_desc: str, scratchpad: str) -> str:
    PROMPT_TEMPLATE = """你是一个智能助理，可以使用工具来回答问题。"""
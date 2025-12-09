
from openai import OpenAI
import pandas as pd
import time

# -------------------
# 初始化 OpenAI 客户端
# -------------------
client = OpenAI(api_key="")

# -------------------
# 20 条 Prompt（第一轮）
# -------------------
prompts = [
    "查询所有客户的姓名和邮箱。",
    "查找所有来自上海（city = 'Shanghai'）的客户。",
    "找出金额大于 500 的订单。",
    "统计订单总数。",
    "按城市统计客户数量。",
    "查询 2024 年创建的订单。",
    "列出所有未支付（pending）的订单 id 和金额。",
    "查询每个客户的订单总金额。",
    "显示每个产品的总销售数量。",
    "找出购买次数最多的客户（按订单数排序）。",
    "查询订单金额最高的前 5 个订单。",
    "查询每个月的订单数量。",
    "查找购买过价格高于 100 的产品的客户。",
    "查询每个客户下单的次数。",
    "列出总消费金额大于 2000 的客户。",
    "计算所有订单的平均金额。",
    "查询销售额最高的商品（按总金额排序）。",
    "显示所有订单及其对应客户的名字。",
    "按状态统计订单数量。",
    "列出购买过 'Laptop' 商品的所有客户。"
]

# -------------------
# 数据库 schema（固定）
# -------------------
schema = """
Database: retail

Table: customers(id, name, email, age, city)
Table: orders(id, customer_id, amount, order_date, status)
Table: products(id, name, price)
Table: order_items(order_id, product_id, quantity)
"""

# -------------------
# 调用模型并记录结果
# -------------------
results = []

print("开始执行 20 条 Prompt ...\n")

for idx, p in enumerate(prompts, start=1):
    print(f"Running Prompt {idx}/20 ...")

    # 给模型的完整提示信息
    full_prompt = f"""
你是一个 SQL 生成模型，请根据以下数据库结构生成 SQL：

{schema}

用户需求：{p}

要求：
- 只输出 SQL，不要解释；
- 必须使用给定 schema 中的字段；
- 保证 SQL 可执行；
"""

    # 调用大模型
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # 你可以换成你想用的模型
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0  # 保证稳定输出
    )

    sql_output = response.choices[0].message.content.strip()
    print(f"SQL Output:\n{sql_output}\n")

    results.append({
        "id": idx,
        "prompt": p,
        "sql": sql_output
    })


# -------------------
df = pd.DataFrame(results)
df.to_csv("sql_generation_round1.csv", encoding="utf-8-sig", index=False)

print("\n全部完成！结果已保存到 sql_generation_round1.csv")

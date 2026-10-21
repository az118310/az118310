#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""手写 Tool Calling 循环 —— Day 11/3 (11/03) 晚间主任务

为什么手写而不是直接用 LangChain:
    框架是把这一百行代码藏起来了。你不亲手写一遍, 永远不知道
    Agent 到底在"思考"什么、什么时候该停、出错时怎么恢复。
    面试官问"Agent 的执行循环是怎么工作的", 你必须能白板画出来。

本文件就是一个最小可用的 Agent:
    用户问题 → 模型判断要不要调工具 → 执行工具 → 把结果塞回上下文 → 再问模型 → 直到模型不再要工具

跑通后你的 TODO:
    1. 加第 3 个工具 (比如 "查物流")
    2. 给工具加错误处理 (模拟工具报错, 看 Agent 能不能自己恢复)
    3. 加一个 max_iterations 上限, 防止死循环
    4. 打印每一步的 thought, 观察模型在想什么

运行:
  export OPENAI_API_KEY=sk-xxx
  python tool_loop.py
"""

import json
import os
import sys
from typing import Any

try:
    from openai import OpenAI
except ImportError:
    print("请先安装依赖: pip install openai", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------------
# 加载 .env（与 basic_call.py 保持一致的实现方式）
# ------------------------------------------------------------------
def load_dotenv(path: str) -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val


_HERE = os.path.dirname(os.path.abspath(__file__))
for _up in range(3):
    _candidate = os.path.join(_HERE, ".env")
    if os.path.exists(_candidate):
        load_dotenv(_candidate)
        break
    _HERE = os.path.dirname(_HERE)


BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

MAX_ITERATIONS = 5  # 防止死循环


# ------------------------------------------------------------------
# 第一部分: 定义工具 (Tools)
# ------------------------------------------------------------------
# 关键认知: 工具定义本身就是给模型看的"说明书"。
# description 写得越清楚, 模型调用得越准。这里偷懒, 模型就会乱调或不该调。
# ------------------------------------------------------------------
TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": (
                "根据关键词搜索淘宝店铺的商品资料。"
                "当客户询问具体商品的信息(价格/材质/尺码/颜色/发货时间)时使用。"
                "不要凭记忆回答商品参数, 必须调用此工具查询。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "商品名称或关键词, 如 '连衣裙' '马克杯'",
                    }
                },
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calc",
            "description": (
                "计算器。用于任何数学运算(加/减/乘/除/百分比)。"
                "当需要精确数字时必须使用本工具, 不要自己心算。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的表达式, 如 '189*2-20' 或 '(189-20)/189'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]


# ------------------------------------------------------------------
# 第二部分: 实现工具 (Tool Implementations)
# ------------------------------------------------------------------
PRODUCT_DB = {
    "连衣裙": {
        "name": "法式复古碎花连衣裙",
        "price": 189.00,
        "materials": "聚酯纤维92% 氨纶8%",
        "sizes": "S/M/L/XL, 常规版型肩窄建议大一码",
        "colors": "雾霾蓝/奶油白/复古红",
        "ship_time": "48小时内发货, 浙江杭州发出",
        "return_policy": "7天无理由退换, 换码来回运费买家承担",
    },
    "马克杯": {
        "name": "简约陶瓷马克杯 400ml",
        "price": 49.00,
        "materials": "高白瓷",
        "sizes": "400ml 直径8.5cm 高9.5cm",
        "colors": "奶白/雾灰/浅杏",
        "ship_time": "24小时内发货, 广东佛山发出",
        "return_policy": "7天无理由退换, 瑕疵品包邮换新",
    },
}


def search_product(keyword: str) -> dict:
    """搜索商品库。查不到就明确返回, 不编造。"""
    for key, value in PRODUCT_DB.items():
        if key in keyword or keyword in key:
            return {"found": True, **value}
    return {
        "found": False,
        "message": f"商品库中没有 '{keyword}'，请告知客户需要核实",
        "available": list(PRODUCT_DB.keys()),
    }


def calc(expression: str) -> dict:
    """安全计算器: 只允许数字和基本运算符。"""
    allowed = set("0123456789+-*/().% ")
    if not set(expression) <= allowed:
        return {"error": f"表达式含非法字符: {expression}"}
    try:
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307 - 已用白名单过滤
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": f"计算失败: {e}"}


TOOL_IMPLS = {
    "search_product": search_product,
    "calc": calc,
}


# ------------------------------------------------------------------
# 第三部分: Agent 主循环 (核心)
# ------------------------------------------------------------------
def run_agent(client: OpenAI, user_input: str) -> str:
    """Agent 执行循环。

    这就是所有 Agent 框架的内核。四步:
      1. 把对话历史 + 工具定义发给模型
      2. 模型返回 tool_calls → 执行工具 → 把结果作为 tool 消息追加进历史
      3. 回到第 1 步
      4. 模型不再返回 tool_calls 时，它给出最终答案，循环结束
    """
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "你是淘宝店铺售前客服助手。\n"
                "规则:\n"
                "1. 涉及商品的具体参数时，必须调用 search_product 工具查询，禁止凭记忆回答。\n"
                "2. 需要计算价格、折扣时，必须调用 calc 工具。\n"
                "3. 查不到的商品不要编造，直接说明需要核实。\n"
                "4. 回复要简洁、口语化，第一句直接回答问题。"
            ),
        },
        {"role": "user", "content": user_input},
    ]

    for iteration in range(MAX_ITERATIONS):
        print(f"\n{'=' * 60}")
        print(f"[Agent 第 {iteration + 1} 轮] 请求模型...")
        print("=" * 60)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",  # 让模型自己决定要不要调工具
            temperature=0.2,
        )
        msg = response.choices[0].message

        # --- 分支 A: 模型要调工具 ---
        if msg.tool_calls:
            # 必须先把 assistant 消息(含 tool_calls)放进历史, 否则下一轮 API 会报错
            messages.append(msg.model_dump(exclude_none=True))

            for call in msg.tool_calls:
                name = call.function.name
                raw_args = call.function.arguments or "{}"
                print(f"  -> 调用工具: {name}({raw_args})")

                impl = TOOL_IMPLS.get(name)
                if impl is None:
                    result = {"error": f"未知工具: {name}"}
                else:
                    try:
                        args = json.loads(raw_args)
                        result = impl(**args)
                    except Exception as e:
                        # 工具报错不要让 Agent 崩掉, 把错误信息喂回模型让它自己纠正
                        result = {"error": f"{type(e).__name__}: {e}"}

                print(f"  <- 工具返回: {json.dumps(result, ensure_ascii=False)[:200]}")

                # 关键: 工具结果必须以 role="tool" 放进历史, 且 tool_call_id 必须匹配
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )
            continue  # 回到循环开头, 让模型看工具结果后继续

        # --- 分支 B: 模型给出最终答案 ---
        print("\n[Agent 完成] 最终回复:")
        print(msg.content)
        return msg.content or ""

    return "已达到最大轮次限制，任务未完成。"


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        print("未检测到 OPENAI_API_KEY 环境变量。", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url=BASE_URL)

    questions = [
        "这款连衣裙多少钱？两件能便宜点吗？",
        "我 165cm 100 斤肩有点宽，应该买 M 还是 L？",
        "随便推荐个 500 块以内的马克杯",
    ]

    for q in questions:
        print("\n" + "#" * 70)
        print(f"# 客户问题: {q}")
        print("#" * 70)
        try:
            run_agent(client, q)
        except Exception as e:
            print(f"出错: {type(e).__name__}: {e}", file=sys.stderr)
            break


if __name__ == "__main__":
    main()

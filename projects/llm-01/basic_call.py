#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""LLM API 最小可运行示例 —— Day 10/21 (10/26) 晚间主任务

目标: 用 30 行代码跑通一次大模型调用, 打印回复。
跑通后, 把 API_KEY 换成你自己的, 改 PROMPT, 观察输出变化。

支持三家国内可直连的 API (改 BASE_URL 和 MODEL 即可切换):

  DeepSeek : BASE_URL="https://api.deepseek.com/v1"    MODEL="deepseek-chat"
  通义千问 : BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
             MODEL="qwen-plus"
  智谱GLM : BASE_URL="https://open.bigmodel.cn/api/paas/v4"
             MODEL="glm-4-flash"

安装依赖:
  pip install openai     # DeepSeek/千问/智谱 都兼容 OpenAI SDK

用法:
  export OPENAI_API_KEY=sk-xxxx
  python basic_call.py
"""

import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print("请先安装依赖: pip install openai", file=sys.stderr)
    sys.exit(1)

# ------------------------------------------------------------------
# 配置区
# ------------------------------------------------------------------
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
API_KEY = os.getenv("OPENAI_API_KEY", "")

PROMPT = """
你是淘宝店铺的售前客服助手。请用一句话回答客户问题，不要客套话。

商品信息:
  名称: 法式复古碎花连衣裙
  价格: 189.00 元
  面料: 聚酯纤维 92%, 氨纶 8%
  尺码: S/M/L/XL (常规版型, 肩窄建议大一码)
  颜色: 雾霾蓝 / 奶油白 / 复古红
  发货: 浙江杭州, 48小时内发货
  退换: 7天无理由, 换码免费承担来回运费

客户问题: "我 165cm 100斤有点肩宽穿 M 还是 L？大概多久能到？"

只输出回答正文。
""".strip()


# ------------------------------------------------------------------
# 主逻辑
# ------------------------------------------------------------------
def main() -> None:
    if not API_KEY:
        print("未检测到 OPENAI_API_KEY 环境变量。", file=sys.stderr)
        print("Windows PowerShell 设置方式: $env:OPENAI_API_KEY='sk-xxx'", file=sys.stderr)
        print("Git Bash 设置方式: export OPENAI_API_KEY=sk-xxx", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一个专业、简洁的电商售前客服。"},
                {"role": "user", "content": PROMPT},
            ],
            temperature=0.3,   # 客服场景要稳定，别发散
            max_tokens=500,
        )
    except Exception as e:
        print(f"调用失败: {type(e).__name__}: {e}", file=sys.stderr)
        print("排查顺序: 1) API_KEY 是否正确 2) BASE_URL 是否正确 "
              "3) 模型名是否存在 4) 账户是否有余额", file=sys.stderr)
        sys.exit(1)

    reply = response.choices[0].message.content
    print("=" * 60)
    print("模型回复:")
    print("=" * 60)
    print(reply)
    print("=" * 60)
    usage = response.usage
    if usage:
        print(f"Token 用量: prompt={usage.prompt_tokens} "
              f"completion={usage.completion_tokens} total={usage.total_tokens}")


if __name__ == "__main__":
    main()

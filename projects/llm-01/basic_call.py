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
# 加载 .env（无需额外依赖，手动解析，避免多装 python-dotenv）
# 优先级：真实环境变量 > .env 文件
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


# 从项目根目录往上找 .env
_HERE = os.path.dirname(os.path.abspath(__file__))
for _up in range(3):
    _candidate = os.path.join(_HERE, ".env")
    if os.path.exists(_candidate):
        load_dotenv(_candidate)
        break
    _HERE = os.path.dirname(_HERE)


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
        print("未检测到 API Key。", file=sys.stderr)
        print("", file=sys.stderr)
        print("推荐做法（写进 .env，一次配置长期有效）:", file=sys.stderr)
        print("  .\\scripts\\py.cmd scripts\\setup_key.py --interactive", file=sys.stderr)
        print("", file=sys.stderr)
        print("临时做法（只对当前窗口有效）:", file=sys.stderr)
        print("  $env:OPENAI_API_KEY='sk-xxx'", file=sys.stderr)
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

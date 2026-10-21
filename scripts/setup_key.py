#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一键配置 LLM API Key —— 写入 .env 文件

用法（在 agent-learning 目录下，PowerShell）：
    .\\scripts\\py.cmd scripts\\setup_key.py

或者交互式（会让你选服务商、粘贴 Key）：
    .\\scripts\\py.cmd scripts\\setup_key.py --interactive

不会把 Key 打印到屏幕，也不会写进 git（.env 已在 .gitignore 中）。
"""

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ENV_FILE = REPO / ".env"

PROVIDERS = {
    "deepseek": {
        "name": "DeepSeek（推荐首选，国内直连，便宜）",
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "key_prefix": "sk-",
        "apply_url": "https://platform.deepseek.com/api_keys",
        "note": "注册后需要充值（最低约 1 元起充），新用户通常有赠送额度",
    },
    "qwen": {
        "name": "通义千问（阿里，有大量免费额度）",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
        "key_prefix": "sk-",
        "apply_url": "https://bailian.console.aliyun.com/",
        "note": "新用户有 100 万 tokens 免费额度，足够学完整个阶段一",
    },
    "zhipu": {
        "name": "智谱 GLM（免费模型 glm-4-flash）",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4-flash",
        "key_prefix": "",
        "apply_url": "https://open.bigmodel.cn/usercenter/apikeys",
        "note": "有免费模型可以无限量调用，适合纯学习练手",
    },
}


def detect_provider(key: str) -> str:
    if key.startswith("sk-"):
        return "unknown"
    if "." in key and key.count(".") == 2 and len(key) == 32:
        return "zhipu"
    return "unknown"


def write_env(provider_key: str, api_key: str) -> None:
    p = PROVIDERS[provider_key]
    content = f"""# LLM API 配置 —— 由 setup_key.py 生成
# 此文件不会被提交到 git（.gitignore 已排除 .env）
LLM_BASE_URL={p['base_url']}
LLM_MODEL={p['model']}
OPENAI_API_KEY={api_key}
"""
    ENV_FILE.write_text(content, encoding="utf-8")
    try:
        os.system(f'attrib +h "{ENV_FILE}"')
    except Exception:
        pass


def interactive() -> None:
    print("\n选择 LLM 服务商：\n")
    keys = list(PROVIDERS.keys())
    for i, k in enumerate(keys, 1):
        p = PROVIDERS[k]
        print(f"  [{i}] {p['name']}")
        print(f"      {p['note']}")
        print(f"      申请地址: {p['apply_url']}")
        print()

    while True:
        choice = input("输入序号 (1-3): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            provider = keys[int(choice) - 1]
            break
        print("请输入 1-3 之间的数字。")

    p = PROVIDERS[provider]
    print(f"\n已选择: {p['name']}")
    print(f"请到 {p['apply_url']} 申请 API Key")
    print("(申请完回来粘贴，粘贴时不会显示字符，属正常现象)\n")

    api_key = input("粘贴 API Key: ").strip()
    if not api_key:
        print("未输入 Key，已取消。")
        return

    write_env(provider, api_key)
    print(f"\n[OK] 已写入 {ENV_FILE}")
    print(f"     BASE_URL = {p['base_url']}")
    print(f"     MODEL    = {p['model']}")
    print("\n下一步：")
    print(f"  .\\scripts\\py.cmd projects\\llm-01\\basic_call.py")
    print("\n如果报 401，把 Key 复制到 https://platform.deepseek.com 确认是否已激活。")


def quick() -> None:
    """从命令行参数读取：setup_key.py <provider> <key>"""
    if len(sys.argv) < 3:
        print("用法: setup_key.py <provider> <api_key>")
        print("provider 可选: " + ", ".join(PROVIDERS.keys()))
        sys.exit(1)
    provider, api_key = sys.argv[1], sys.argv[2]
    if provider not in PROVIDERS:
        print(f"未知服务商: {provider}，可选: {', '.join(PROVIDERS.keys())}")
        sys.exit(1)
    write_env(provider, api_key)
    print(f"[OK] 已写入 {ENV_FILE}")


if __name__ == "__main__":
    if "--interactive" in sys.argv or "-i" in sys.argv:
        interactive()
    elif len(sys.argv) >= 3:
        quick()
    else:
        interactive()

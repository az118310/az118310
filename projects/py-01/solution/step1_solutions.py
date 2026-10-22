#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Step 1 完整答案 —— 卡住超过 20 分钟再看这个文件
=================================================

重要：看懂 ≠ 学会。
看完答案后，关掉这个文件，把答案**默写**进 step1_basics.py，
然后删掉这里对应的 TODO 标记，再跑一遍。

如果只是复制粘贴，你会以为你会了，考试时一样懵。
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 本文件在 solution/ 子目录里，数据在上一级 ../data/
DATA_FILE = os.path.join(os.path.dirname(BASE_DIR), "data", "tickets.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

print(f"[1] 文件字符数: {len(raw_text)}")

tickets = json.loads(raw_text)

print(f"[2] 工单条数: {len(tickets)}")
print(f"    第一条的 id: {tickets[0]['id']}")
print(f"    最后一条的 id: {tickets[-1]['id']}")

# --- 第 3 题答案 ---
first = tickets[0]
print("\n[3] 第一条工单的字段:")
for key in first:
    print(f"    - {key}: {first[key]}")

# --- 第 4 题答案 ---
print("\n[4] 所有工单概要:")
for t in tickets:
    print(f"    {t['id']} | {t['customer']} | {t['product']}")

# --- 第 5 题答案 ---
pending = []
for t in tickets:
    if t["status"] == "pending":
        pending.append(t)

print(f"\n[5] 待处理工单: {len(pending)} 条")

# --- 第 6 题答案 ---
counts = {}
for t in pending:
    intent = t["intent"]
    counts[intent] = counts.get(intent, 0) + 1

print("[6] 待处理工单的意图分布:")
for intent, n in counts.items():
    print(f"    {intent}: {n} 条")

# --- 第 7 题答案（两种写法都给你）---
# 写法 A：显式循环（更好懂，推荐先用这个）
risk_amount = 0
for t in pending:
    if t["intent"] == "quality_complaint":
        risk_amount += t["price"]

# 写法 B：列表推导式 + sum（更 Pythonic，面试加分）
risk_amount_b = sum(
    t["price"] for t in pending if t["intent"] == "quality_complaint"
)

print(f"\n[7] 质量投诉类待处理工单金额合计: {risk_amount:.2f} 元")
print(f"    (列表推导式写法结果一致: {risk_amount_b:.2f} 元)")

# ==================================================================
# 关键语法点复盘
# ==================================================================
print("\n" + "=" * 60)
print("语法要点")
print("=" * 60)

print("""
1. 列表下标
   tickets[0]   → 第一条
   tickets[-1]  → 最后一条
   tickets[0:3] → 前三条（切片，左闭右开）

2. 字典取值
   t["id"]            → 取值
   t.get("id")        → 取值，键不存在返回 None（不报错）
   t.get("id", "默认") → 取值，键不存在返回默认值

3. == 和 = 的区别
   =  是赋值（把右边的值给左边）
   == 是比较（判断两边是否相等）

4. 遍历字典
   for key in d:          → 遍历键
   for value in d.values():  → 遍历值
   for k, v in d.items():    → 遍历键值对

5. f-string
   f"{变量}"          → 插入值
   f"{变量:.2f}"      → 保留两位小数
   f"{变量:>10}"      → 右对齐占 10 格

6. 缩进是语法
   Python 用缩进表示代码块，4 个空格。
   if/for/while 下面的代码必须缩进，否则 IndentationError。
""")

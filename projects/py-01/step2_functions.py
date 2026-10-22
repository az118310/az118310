#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Step 2 · 函数与文件写入
=================================================

Step 1 你已经能读数据、筛选、统计了。
但那些代码写完就扔——下一份报表还要复制粘贴一遍。

Step 2 学两件事：
  1. 函数 = 把一段逻辑打包，给它起个名字，反复调用
  2. 写文件 = 把处理结果存成 JSON，下次直接读

场景：把「待处理工单」整理成一份客服日报存到磁盘。

前置：先完成 step1_basics.py
运行： .\\scripts\\py.cmd projects\\py-01\\step2_functions.py
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "tickets.json")
REPORT_FILE = os.path.join(BASE_DIR, "data", "daily_report.json")


# ==================================================================
# Part A · 函数基础
# ==================================================================

# 函数定义的固定写法：
#   def 函数名(参数):
#       函数体（缩进 4 空格）
#   return 返回值
#
# 注意 def 后面有冒号，函数体必须缩进。

def count_by(tickets: list, field: str) -> dict:
    """按某个字段统计出现次数。

    参数:
        tickets: 工单列表
        field:   要统计的字段名，比如 "intent"
    返回:
        形如 {"shipping": 2, "size_advice": 1} 的字典
    """
    counts = {}
    for t in tickets:
        key = t[field]
        counts[key] = counts.get(key, 0) + 1
    return counts


def filter_by(tickets: list, **conditions) -> list:
    """按多个条件筛选工单。

    用法:
        filter_by(tickets, status="pending")
        filter_by(tickets, status="pending", urgency="high")

    **conditions 表示"接收任意个关键字参数"，装在一个字典里。
    """
    result = []
    for t in tickets:
        # TODO: 补上判断逻辑——只有当工单的所有条件都满足时，才加进 result
        # 提示：遍历 conditions.items()，拿 (k, v) 对，比较 t[k] == v
        # 所有条件都满足才算命中，所以需要一个"全部满足"的标志
        pass
    return result


def total_amount(tickets: list, intent: str) -> float:
    """统计某个意图类别的订单总金额。

    这是加分项：列表推导式 + sum()，一行搞定。
    """
    return sum(t["price"] for t in tickets if t["intent"] == intent)


# ==================================================================
# Part B · 读取数据 + 调用函数
# ==================================================================

with open(DATA_FILE, "r", encoding="utf-8") as f:
    tickets = json.loads(f.read())

print(f"读入 {len(tickets)} 条工单")

# --- 验证 count_by ---
pending = filter_by(tickets, status="pending")
print(f"\n[A] 待处理工单: {len(pending)} 条")

if not pending:
    print("!!! filter_by 还没写对，先补全 TODO 再往下走")
    raise SystemExit(1)

intent_counts = count_by(pending, "intent")
print("[A] 意图分布:")
for k, v in intent_counts.items():
    print(f"    {k}: {v}")

# TODO（选做）: 再试几个组合，比如
#   high = filter_by(tickets, status="pending", urgency="high")
#   print("紧急待处理:", len(high))


# ==================================================================
# Part C · 写文件：生成日报
# ==================================================================

# 报告结构
report = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_tickets": len(tickets),
    "pending_count": len(pending),
    "intent_distribution": intent_counts,
    "risk_amount": round(total_amount(pending, "quality_complaint"), 2),
    "urgent_tickets": [],
}

# TODO: 把"紧急"工单（urgency == "high" 且 status == "pending"）的
#       id / customer / product / message 整理进 report["urgent_tickets"]
# 每个工单存成 {"id": ..., "customer": ..., "product": ..., "message": ...}
# 提示：先 filter_by 拿到列表，然后 for 循环构建字典

print("\n[C] 紧急工单:")
for t in filter_by(tickets, status="pending", urgency="high"):
    print(f"    {t['id']} | {t['customer']} | {t['message']}")


# ==================================================================
# Part D · 写文件
# ==================================================================

# json.dump(数据, 文件对象, indent=2, ensure_ascii=False)
#   indent=2           → 缩进 2 格，可读性好（写文件必加）
#   ensure_ascii=False → 中文不转义成 \uXXXX（不写的话中文全变乱码）

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n[D] 报告已写入: {REPORT_FILE}")

# --- 立刻读回来验证 ---
with open(REPORT_FILE, "r", encoding="utf-8") as f:
    loaded = json.loads(f.read())

print("[D] 读回验证:")
print(f"    待处理: {loaded['pending_count']} 条")
print(f"    风险金额: {loaded['risk_amount']} 元")
print(f"    紧急工单: {len(loaded['urgent_tickets'])} 条")
print(f"    生成时间: {loaded['generated_at']}")


# ==================================================================
# Part E · 加分：异常处理
# ==================================================================

# 文件不存在 / JSON 格式错误都会让程序崩掉。
# try/except 让程序优雅降级，而不是直接退出。

def load_tickets_safe(path: str) -> list:
    """安全读取工单文件，失败时返回空列表而不是崩溃。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print(f"[E] 文件不存在: {path}")
        return []
    except json.JSONDecodeError as e:
        print(f"[E] JSON 格式错误: {e}")
        return []


# 测试一下：故意传一个不存在的文件
missing = load_tickets_safe(os.path.join(BASE_DIR, "data", "nope.json"))
print(f"[E] 不存在的文件返回: {missing} (程序没崩)")

# TODO（选做）: 故意把 tickets.json 的内容改坏，跑一次看 json.JSONDecodeError

print("\n" + "=" * 60)
print("Step 2 预期结果")
print("=" * 60)
print("""
[A] 待处理工单: 6 条
    意图分布: size_advice 1 / shipping 2 / quality_complaint 2 / presale 1
[C] 紧急工单: 3 条
    T20261001002 爱睡觉的鱼（催发货）
    T20261001003 不吃香菜的兔子（质量问题）
    T20261001008 打工人小张（要求退）
[D] 读回验证: 待处理 6 条 / 风险金额 398.0 元 / 紧急工单 3 条
[E] 不存在的文件返回: [] （程序没崩）

跑通后打开 data/daily_report.json 看一眼，那是你的第一份"程序产出物"。
""")

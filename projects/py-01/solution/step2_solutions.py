#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Step 2 完整答案
===============

Step 2 的关键就两处 TODO：
  1. filter_by 的多条件筛选
  2. report["urgent_tickets"] 的构建

其他部分（count_by / total_amount / 写文件 / 异常处理）已经给全了。
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(os.path.dirname(BASE_DIR), "data", "tickets.json")
REPORT_FILE = os.path.join(os.path.dirname(BASE_DIR), "data", "daily_report.json")


def count_by(tickets: list, field: str) -> dict:
    counts = {}
    for t in tickets:
        key = t[field]
        counts[key] = counts.get(key, 0) + 1
    return counts


def filter_by(tickets: list, **conditions) -> list:
    """多条件筛选——所有条件都满足才算命中。"""
    result = []
    for t in tickets:
        matched = True          # 标志位：默认假设全部满足
        for k, v in conditions.items():
            if t.get(k) != v:   # 只要有一个条件不满足
                matched = False
                break           # 就不用再看后面的条件了
        if matched:
            result.append(t)
    return result


def total_amount(tickets: list, intent: str) -> float:
    return sum(t["price"] for t in tickets if t["intent"] == intent)


with open(DATA_FILE, "r", encoding="utf-8") as f:
    tickets = json.loads(f.read())

print(f"读入 {len(tickets)} 条工单")

pending = filter_by(tickets, status="pending")
print(f"\n[A] 待处理工单: {len(pending)} 条")

intent_counts = count_by(pending, "intent")
print("[A] 意图分布:")
for k, v in intent_counts.items():
    print(f"    {k}: {v}")

high = filter_by(tickets, status="pending", urgency="high")
print(f"    紧急待处理: {len(high)} 条")


report = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_tickets": len(tickets),
    "pending_count": len(pending),
    "intent_distribution": intent_counts,
    "risk_amount": round(total_amount(pending, "quality_complaint"), 2),
    "urgent_tickets": [],
}

# 构建紧急工单列表
for t in filter_by(tickets, status="pending", urgency="high"):
    report["urgent_tickets"].append({
        "id": t["id"],
        "customer": t["customer"],
        "product": t["product"],
        "message": t["message"],
    })

print("\n[C] 紧急工单:")
for t in filter_by(tickets, status="pending", urgency="high"):
    print(f"    {t['id']} | {t['customer']} | {t['message']}")


with open(REPORT_FILE, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n[D] 报告已写入: {REPORT_FILE}")

with open(REPORT_FILE, "r", encoding="utf-8") as f:
    loaded = json.loads(f.read())

print("[D] 读回验证:")
print(f"    待处理: {loaded['pending_count']} 条")
print(f"    风险金额: {loaded['risk_amount']} 元")
print(f"    紧急工单: {len(loaded['urgent_tickets'])} 条")
print(f"    生成时间: {loaded['generated_at']}")


def load_tickets_safe(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print(f"[E] 文件不存在: {path}")
        return []
    except json.JSONDecodeError as e:
        print(f"[E] JSON 格式错误: {e}")
        return []


missing = load_tickets_safe(os.path.join(os.path.dirname(BASE_DIR), "data", "nope.json"))
print(f"[E] 不存在的文件返回: {missing} (程序没崩)")

print("\n" + "=" * 60)
print("Step 2 语法要点")
print("=" * 60)
print("""
1. 函数定义
   def 函数名(参数1, 参数2=默认值):
       函数体
       return 值

2. 类型注解（可选但建议写）
   def f(tickets: list, field: str) -> dict:
   → 提示编辑器和 IDE 类型，不影响运行

3. **kwargs
   def f(tickets, **conditions):
   → 调用 f(tickets, status="pending", urgency="high")
   → 函数内 conditions 是 {"status": "pending", "urgency": "high"}

4. 标志位模式（筛选的标准写法）
   matched = True
   for k, v in conditions.items():
       if t.get(k) != v:
           matched = False
           break
   if matched:
       result.append(t)

5. 写 JSON 的两个参数，缺一不可
   json.dump(report, f, indent=2, ensure_ascii=False)
              ↑ 可读        ↑ 中文不转义

6. 异常处理三件套
   try:      尝试执行
   except 具体异常类型:  捕获并处理
   finally:  无论成功失败都执行

   常见异常：
   FileNotFoundError   文件不存在
   JSONDecodeError     JSON 格式错误
   KeyError            字典键不存在
   ValueError          值类型不对（比如 int("abc")）
""")

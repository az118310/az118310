#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动批改 —— 你写完 Step1/Step2 后跑这个，不用肉眼比对输出
=============================================================

用法（在 agent-learning 目录下，PowerShell）：
    .\\scripts\\py.cmd projects\\py-01\\check_my_work.py

它会：
  1. 检查 step1_basics.py 里是否还残留 ???
  2. 跑一遍你的代码，看输出对不对
  3. 逐项打分，告诉你哪一题错了
"""

import json
import os
import re
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))   # agent-learning/

# 用哪个 Python 解释器跑
PY_EXE = sys.executable


def run_script(path: str) -> tuple:
    """运行脚本，返回 (退出码, 输出文本)"""
    try:
        r = subprocess.run(
            [PY_EXE, path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        # 统一换行符为 \n，避免 \r 影响正则匹配
        out = (r.stdout + r.stderr).replace("\r\n", "\n").replace("\r", "\n")
        return r.returncode, out
    except subprocess.TimeoutExpired:
        return 1, "超时（60秒）"
    except Exception as e:
        return 1, f"运行失败: {e}"


def check_no_todo(path: str) -> list:
    """检查文件里还有哪些 TODO 没填（只看真正的代码行）"""
    if not os.path.exists(path):
        return ["文件不存在"]
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    problems = []
    in_docstring = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 跟踪三引号文档字符串的开关
        quote_count = stripped.count('"""') + stripped.count("'''")
        if in_docstring:
            if quote_count % 2 == 1:
                in_docstring = False
            continue
        if quote_count % 2 == 1:
            in_docstring = True
            continue
        if stripped.startswith("#"):
            continue
        if "???" in line:
            problems.append(f"  第 {i} 行还有 ??? 未填: {stripped[:60]}")
    return problems


def check_pass_todo(path: str) -> list:
    """检查还有哪些 TODO 位置留着 pass（写了骨架但没填逻辑）"""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    problems = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == "pass":
            problems.append(f"  第 {i} 行还是 pass（逻辑没写）")
    return problems


print("=" * 64)
print("自动批改")
print("=" * 64)

total_score = 0
max_score = 0
results = []

# ---------------- Step 1 ----------------
print("\n[Step 1] 变量 / 列表 / 字典")
print("-" * 64)

step1 = os.path.join(BASE_DIR, "step1_basics.py")
todos = check_no_todo(step1)
if todos:
    print("  [TODO 未完成]")
    for t in todos:
        print(t)
    print("  → 先把所有 ??? 填掉再跑批改")
else:
    code, out = run_script(step1)
    if code != 0:
        print(f"  [FAIL] 程序报错退出 (exit={code})")
        for line in out.strip().split("\n")[-12:]:
            print(f"    {line}")
    else:
        checks = [
            ("工单条数 = 10", re.search(r"工单条数[:：]\s*10", out) is not None),
            ("第一条 id 正确", re.search(r"第一条的 id[:：]\s*T20261001001", out) is not None),
            ("最后一条 id 正确", re.search(r"最后一条的 id[:：]\s*T20261001010", out) is not None),
            ("字段遍历输出 10 行", len(re.findall(r"^\s+-\s+\w+:", out, re.M)) == 10),
            ("概要输出 10 行", len(re.findall(r"T202610010\d\d \| ", out)) == 10),
            ("待处理 = 6 条", re.search(r"待处理工单[:：]\s*6", out) is not None),
            ("意图分布正确", all(
                re.search(p, out) for p in [
                    r"size_advice[:：]\s*1", r"shipping[:：]\s*2",
                    r"quality_complaint[:：]\s*2", r"presale[:：]\s*1",
                ]
            )),
            ("风险金额 = 398.00", re.search(r"金额合计[:：]\s*398\.00", out) is not None),
        ]
        for name, ok in checks:
            max_score += 1
            if ok:
                total_score += 1
                print(f"  [PASS] {name}")
            else:
                print(f"  [FAIL] {name}")
        results.append(("Step 1", total_score, sum(1 for _, o in checks if o)))

# ---------------- Step 2 ----------------
print("\n[Step 2] 函数 / 文件写入 / 异常处理")
print("-" * 64)

step2 = os.path.join(BASE_DIR, "step2_functions.py")
todos = check_no_todo(step2) + check_pass_todo(step2)
if todos:
    print("  [TODO 未完成]")
    for t in todos:
        print(t)
else:
    code, out = run_script(step2)
    if code != 0:
        print(f"  [FAIL] 程序报错退出 (exit={code})")
        for line in out.strip().split("\n")[-12:]:
            print(f"    {line}")
    else:
        report_file = os.path.join(BASE_DIR, "data", "daily_report.json")
        checks = [
            ("待处理 = 6 条", re.search(r"待处理工单[:：]\s*6", out) is not None),
            ("意图分布正确", all(
                re.search(p, out) for p in [
                    r"size_advice[:：]\s*1", r"shipping[:：]\s*2",
                    r"quality_complaint[:：]\s*2", r"presale[:：]\s*1",
                ]
            )),
            ("紧急工单 = 3 条", len(re.findall(r"T202610010\d\d \| ", out)) == 3),
            ("日报文件已生成", os.path.exists(report_file)),
        ]
        if os.path.exists(report_file):
            try:
                with open(report_file, "r", encoding="utf-8") as f:
                    rep = json.load(f)
                checks.append(("日报内容正确",
                    rep.get("pending_count") == 6
                    and rep.get("risk_amount") == 398.0
                    and len(rep.get("urgent_tickets", [])) == 3))
                checks.append(("日报中文未乱码",
                    any("一" in str(v) or "爱" in str(v)
                        for v in rep.get("urgent_tickets", []))))
            except Exception as e:
                checks.append(("日报内容正确", False))
                checks.append(("日报中文未乱码", False))
        checks.append(("异常处理生效（文件不存在不崩）", "程序没崩" in out))

        s2 = 0
        for name, ok in checks:
            max_score += 1
            if ok:
                total_score += 1
                s2 += 1
                print(f"  [PASS] {name}")
            else:
                print(f"  [FAIL] {name}")
        results.append(("Step 2", s2, len(checks)))

# ---------------- 汇总 ----------------
print("\n" + "=" * 64)
if max_score == 0:
    print("还没有可批改的内容 —— 先把 ??? 填掉。")
    print("卡住超过 20 分钟再看 solution/ 下的答案文件。")
else:
    print(f"得分: {total_score} / {max_score}")
    if total_score == max_score:
        print("全部通过 —— Step 1+2 通关！")
        print("下一步：把今天的成果 git commit，然后开 Step 3（类与面向对象）")
    else:
        print("有未通过项。对照报错信息改，别急着看答案。")
print("=" * 64)

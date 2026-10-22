#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
关卡自动批改
============

用法（在 agent-learning 目录下）：
    .\\scripts\\py.cmd projects\\py-01\\levels\\check.py
    .\\scripts\\py.cmd projects\\py-01\\levels\\check.py L1    ← 只批改第 1 关

怎么判分：
  1. 检查你填的关卡里还有没有 ___ 占位符
  2. 跑一遍你的代码
  3. 跟标准答案版的输出逐行对比
  4. 对上了 = PASS

为什么用"跟答案版对比"而不是写一堆正则：
  正则会因为格式变动就误判，对比输出才准。
"""

import difflib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY_EXE = sys.executable

LEVELS = [
    ("L1", "L1_variables.py", "L1_solution.py"),
    ("L2", "L2_strings.py", "L2_solution.py"),
    ("L3", "L3_lists.py", "L3_solution.py"),
    ("L4", "L4_dicts.py", "L4_solution.py"),
    ("L5", "L5_conditions.py", "L5_solution.py"),
]


def find_placeholders(path: str) -> list:
    """找出还没填的地方（___ 占位符 或 TODO 标记）"""
    if not os.path.exists(path):
        return [("?", "文件不存在")]
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pending = []
    in_doc = False
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        q = s.count('"""') + s.count("'''")
        if in_doc:
            if q % 2 == 1:
                in_doc = False
            continue
        if q % 2 == 1:
            in_doc = True
            continue

        code_part = ln.split("#")[0]
        # 行内 TODO（代码后跟的）才算待填；独立成行的 # TODO 是题目说明
        if "TODO" in ln and code_part.strip():
            pending.append((i, s[:70]))
            continue
        if "___" in code_part:
            pending.append((i, s[:70]))
    return pending


def run(path: str) -> tuple:
    try:
        r = subprocess.run(
            [PY_EXE, path], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=60,
        )
        out = (r.stdout + r.stderr).replace("\r\n", "\n").replace("\r", "\n")
        return r.returncode, out
    except subprocess.TimeoutExpired:
        return 1, "超时"
    except Exception as e:
        return 1, f"运行失败: {e}"


def normalize(text: str) -> list:
    """去掉噪音行，只留有意义的输出"""
    lines = []
    for ln in text.split("\n"):
        s = ln.strip()
        if not s:
            continue
        # 跳过生成时间这类每次都变的内容
        if "生成时间" in s or "generated_at" in s:
            continue
        # 跳过含文件路径的警告行（骨架和答案所在目录不同，路径必然不一致）
        if "Warning" in s:
            continue
        # 跳过 docstring 里带路径的说明行
        if "py.cmd" in s or "运行：" in s:
            continue
        lines.append(s)
    return lines


def main() -> None:
    only = sys.argv[1].upper() if len(sys.argv) > 1 else None

    print("=" * 64)
    print("关卡自动批改")
    print("=" * 64)

    total = 0
    earned = 0
    all_pass = True

    for key, skel, sol in LEVELS:
        if only and only != key:
            continue

        print(f"\n[{key}] {skel}")
        print("-" * 64)

        skel_path = os.path.join(HERE, skel)
        sol_path = os.path.join(HERE, "solution", sol)

        if not os.path.exists(skel_path):
            print("  [跳过] 文件不存在")
            continue

        pending = find_placeholders(skel_path)
        if pending:
            print(f"  [还有 {len(pending)} 处没填]")
            for ln, txt in pending:
                print(f"    第 {ln} 行: {txt}")
            print("  → 先填完再批改。卡住 20 分钟看文件末尾【答案】。")
            all_pass = False
            continue

        if not os.path.exists(sol_path):
            print("  [跳过] 没有标准答案版，无法对比")
            continue

        code, my_out = run(skel_path)
        if code != 0:
            print(f"  [FAIL] 程序报错退出 (exit={code})")
            for ln in my_out.strip().split("\n")[-10:]:
                print(f"    {ln}")
            all_pass = False
            continue

        _, ref_out = run(sol_path)
        mine = normalize(my_out)
        ref = normalize(ref_out)

        if mine == ref:
            total += 1
            earned += 1
            print(f"  [PASS] 输出与标准答案完全一致（{len(mine)} 行）")
            print(f"  → {key} 通关！")
        else:
            all_pass = False
            print("  [FAIL] 输出和标准答案不一致")
            print("  差异如下（- 是你的，+ 是正确的）：")
            diff = list(difflib.unified_diff(ref, mine, "标准答案", "你的输出", lineterm="", n=1))
            for ln in diff[:30]:
                print(f"    {ln}")

    print("\n" + "=" * 64)
    if total == 0:
        print("没有可批改的内容 —— 先把 ___ 填掉。")
    elif all_pass and earned == total:
        print(f"全对！{earned} / {total}")
        print("下一步：git commit，然后开下一关。")
    else:
        print(f"得分: {earned} / {total}（还有关卡没过）")
    print("=" * 64)


if __name__ == "__main__":
    main()

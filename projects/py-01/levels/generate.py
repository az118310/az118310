#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
关卡生成器 —— 一份模板，同时产出「骨架版」和「答案版」
===========================================================

模板放在同目录的 templates/ 里，一个关卡一个文件（L1.tpl ~ L5.tpl）。
骨架和答案必须逐字对应，手工维护两份文件早晚会不一致（已踩坑三次）。

标记约定
--------
  @@答案@@      → 骨架版变成 ___，答案版填入答案
  @@C:代码@@    → 骨架版是「代码」，答案版是「# 代码」（整行注释掉）
  @@R:旧::新@@  → 骨架版用「旧」，答案版用「新」
                  （用于"学生要改成什么样"这种题，答案版必须是改完后的样子）
  @@GUARD@@     → 骨架版的占位符检查器，答案版自动移除

为什么不用 {xxx}：Python 的 f-string 会把 {xxx} 当表达式解析，
                  模板本身就会报语法错误。@@ 在 Python 里不可能出现，绝对安全。

答案必须是能直接跑的代码。字符串自己带引号（@@"商品"@@），生成器不猜。

保护机制
--------
  骨架版一旦被你改过（填了答案、改了注释），生成器默认不覆盖它。
  判定方式：把磁盘上的文件跟「模板展开结果」逐字比。
  不一样 = 你动过 = 不碰。真要重置某一关，加 --force。

用法
----
  .\\scripts\\py.cmd projects\\py-01\\levels\\generate.py
      只重生成答案版（安全，永远不会碰你的作答）

  .\\scripts\\py.cmd projects\\py-01\\levels\\generate.py --skeleton L3 L4
      重生成指定关卡的骨架版（会清空这些关卡的作答，慎用）

  .\\scripts\\py.cmd projects\\py-01\\levels\\generate.py --skeleton --force
      强制重生成骨架版，不管你改没改过
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL_DIR = os.path.join(HERE, "templates")
OUT = os.path.join(HERE, "solution")

GUARD = "from guard import check\nimport os\n\ncheck(os.path.abspath(__file__))\n"

LEVELS = [
    ("L1", "L1_variables.py", "L1_solution.py"),
    ("L2", "L2_strings.py", "L2_solution.py"),
    ("L3", "L3_lists.py", "L3_solution.py"),
    ("L4", "L4_dicts.py", "L4_solution.py"),
    ("L5", "L5_conditions.py", "L5_solution.py"),
]


# ----------------------------------------------------------------------
# 展开
# ----------------------------------------------------------------------

def skeleton_text(src: str) -> str:
    """模板 → 骨架版（不写盘）"""
    out = re.sub(r"@@C:(.*?)@@", lambda m: m.group(1), src, flags=re.S)
    out = re.sub(r"@@R:(.*?)::(.*?)@@", lambda m: m.group(1), out, flags=re.S)
    out = re.sub(r"@@([^@]*)@@", "___", out)
    return out.replace("@@", "___")


def solution_text(src: str) -> str:
    """模板 → 答案版（不写盘）"""
    out = src

    # 整行注释掉
    out = re.sub(r"@@C:(.*?)@@", lambda m: "# " + m.group(1), out, flags=re.S)

    # 新旧替换
    out = re.sub(r"@@R:(.*?)::(.*?)@@", lambda m: m.group(2), out, flags=re.S)

    def repl(m):
        ans = m.group(1)
        before = out[:m.start()]
        line_start = before.rfind("\n") + 1
        line_prefix = before[line_start:].rstrip()

        # 已经带引号了（'...' 或 "..."）→ 原样输出
        if ans.startswith(("'", '"')):
            return ans

        prev = before.rstrip()[-1:] if before.strip() else ""
        is_after_colon = prev == ":"          # 字典 / JSON 的键值位置
        is_assignment = line_prefix.endswith("=")

        # 已经是合法表达式（含括号/点/引号/数字/方括号）→ 不加引号
        is_expression = bool(re.search(r"[()\[\].'\d]", ans))

        if (is_assignment or is_after_colon) and not is_expression:
            return f'"{ans}"'
        return ans

    out = re.sub(r"@@([^@]*)@@", repl, out)
    out = out.replace("@@", "")
    # 用等量空行替换 GUARD，保证答案版和骨架版行号一一对应
    out = out.replace(GUARD, "\n" * GUARD.count("\n"))
    # 答案版不该再有行内 TODO 标记
    out = re.sub(r"[ \t]*#[ \t]*TODO[^\n]*", "", out)
    return out


def write(path: str, text: str) -> None:
    # Windows 上写 CRLF，跟你用记事本 / VS Code 编辑的结果一致，
    # 这样 git diff 只看真实内容改动，不会整文件变红
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(text)
    print(f"  {path}")


def norm(text: str) -> str:
    """比对用：忽略行尾符差异"""
    return text.replace("\r\n", "\n").replace("\r", "\n")


# ----------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    os.makedirs(OUT, exist_ok=True)

    want_skeleton = "--skeleton" in args
    force = "--force" in args
    targets = [a.upper() for a in args if not a.startswith("--")]

    print("生成答案版（永远不会影响你的作答）：")
    for key, skel_name, sol_name in LEVELS:
        tpl_path = os.path.join(TPL_DIR, f"{key}.tpl")
        if not os.path.exists(tpl_path):
            print(f"  [跳过] {key} 模板不存在: {tpl_path}")
            continue
        with open(tpl_path, "r", encoding="utf-8") as f:
            src = f.read().replace("@@GUARD@@", GUARD)
        write(os.path.join(OUT, sol_name), solution_text(src))

    if not want_skeleton:
        print("\n骨架版没动（想重生成加 --skeleton，会清空作答）")
        return

    print("\n生成骨架版：")
    for key, skel_name, sol_name in LEVELS:
        if targets and key not in targets:
            continue
        tpl_path = os.path.join(TPL_DIR, f"{key}.tpl")
        with open(tpl_path, "r", encoding="utf-8") as f:
            src = f.read().replace("@@GUARD@@", GUARD)

        preview = skeleton_text(src)
        path = os.path.join(HERE, skel_name)

        if os.path.exists(path) and not force:
            with open(path, "r", encoding="utf-8", newline="") as f:
                on_disk = f.read()
            if norm(on_disk) != norm(preview):
                print(f"  [跳过] {skel_name}（你改过了，不覆盖；确实要重置加 --force）")
                continue

        write(path, preview)


if __name__ == "__main__":
    main()

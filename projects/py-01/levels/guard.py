#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
占位符检查器（所有关卡共用，别改这个文件）
============================================

作用：每关开头写一行 `from guard import check`，然后调用 `check(__file__)`。
如果文件里还有没填的 ___ 占位符，它会：
  1. 打印清单（哪一行还没填）
  2. 直接退出，不让你看到一堆看不懂的报错

为什么用 ___ 而不是 ???：
  ??? 放在 f-string 里会导致语法错误，你还没开始写就崩了。
  ___ 是合法标识符，能安全地出现在任何位置。

怎么用：
  把关卡文件里的 ___ 换成你的答案就行。
"""

import os
import sys


def check(file_path: str) -> None:
    """检查文件里是否还有待填标记，有则打印清单并退出。

    两种待填标记：
      1. `___`  —— 变量/表达式位置的占位符
      2. `TODO` —— 需要修改的行（行内已有 TODO 注释）
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pending = []
    in_doc = False

    for i, ln in enumerate(lines, 1):
        s = ln.strip()

        # 三引号文档字符串内的说明不算
        q = s.count('"""') + s.count("'''")
        if in_doc:
            if q % 2 == 1:
                in_doc = False
            continue
        if q % 2 == 1:
            in_doc = True
            continue

        # 行内 TODO 标记（代码后面跟的 # TODO ...）
        # 独立成行的 "# TODO ..." 是题目说明，不算待填
        code_part = ln.split("#")[0]
        if "TODO" in ln and code_part.strip():
            pending.append((i, s[:70]))
            continue

        # ___ 占位符
        if "___" in code_part:
            pending.append((i, s[:70]))

    if pending:
        print("=" * 62)
        print(f"还有 {len(pending)} 处没填")
        print("=" * 62)
        for i, s in pending:
            print(f"  第 {i} 行: {s}")
        print()
        print("填完后重新运行本文件。答案在文件末尾的【答案】区。")
        print("=" * 62)
        sys.exit(0)


if __name__ == "__main__":
    # 直接运行本文件时，检查同目录下的所有关卡
    here = os.path.dirname(os.path.abspath(__file__))
    for fn in sorted(os.listdir(here)):
        if fn.startswith("L") and fn.endswith(".py"):
            print(f"\n### {fn}")
            check(os.path.join(here, fn))

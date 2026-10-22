# py-01 · 客服工单处理器（Day 1 项目）

> **目标**：不学语法大全，就做一个你每天都在干的事——处理客服工单。
> 做完你会真的写 Python 了，不是"看懂了"。

---

## 怎么用

```powershell
cd D:\app\2026-10-21-21-42-36\agent-learning

# 1. 跑 Step 1（骨架版，先看它现在是什么样）
.\scripts\py.cmd projects\py-01\step1_basics.py

# 2. 打开 projects\py-01\step1_basics.py，把所有 ??? 换成你的答案

# 3. 再跑一次，看结果对不对
.\scripts\py.cmd projects\py-01\step1_basics.py

# 4. 自动批改（不用肉眼比对了）
.\scripts\py.cmd projects\py-01\check_my_work.py
```

**卡住超过 20 分钟**再看 `solution/step1_solutions.py`。
**看懂 ≠ 学会**——看完答案要关掉它，默写一遍，再跑。

---

## 文件说明

| 文件 | 作用 |
|---|---|
| `data/tickets.json` | 10 条模拟工单，字段和真实客服工单一样 |
| `step1_basics.py` | **你的作业** · 变量/列表/字典 |
| `step2_functions.py` | **你的作业** · 函数/文件写入/异常处理 |
| `check_my_work.py` | 自动批改，15 分制 |
| `solution/step1_solutions.py` | 答案（卡住再看） |
| `solution/step2_solutions.py` | 答案（卡住再看） |

---

## Step 1 · 你要做的 7 件事

| # | 考点 | 对应你的真实工作 |
|---|---|---|
| 1 | 读文件 | 打开工单表 |
| 2 | JSON → Python | 系统导出的数据变成可用对象 |
| 3 | 字典遍历 | 看一条工单的每个字段 |
| 4 | for 循环 | 逐条过工单 |
| 5 | if 筛选 | 只留待处理的 |
| 6 | 字典计数 | 统计各意图多少条 |
| 7 | 加分：求和 | 算出质量投诉的金额风险 |

**验收**：待处理 6 条、意图分布 1/2/2/1、风险金额 398.00 元

---

## Step 2 · 你要做的 4 件事

| # | 考点 | 为什么重要 |
|---|---|---|
| A | 函数定义 + `**kwargs` | `filter_by(tickets, status="pending", urgency="high")` 这种写法是面试高频 |
| B | 调用函数 | 把 Step 1 的逻辑复用起来 |
| C | 构建字典列表 | 整理成结构化数据 |
| D | 写 JSON 文件 | `json.dump(..., indent=2, ensure_ascii=False)` 两个参数缺一不可 |
| E | 加分：异常处理 | 文件不存在/格式错，程序不崩而是优雅降级 |

**验收**：生成 `data/daily_report.json`，里面含待处理数、意图分布、风险金额、紧急工单列表

---

## 遇到报错怎么办

**三步定位法**（报错信息从下往上读）：

```
Traceback (most recent call last):
  File "step1_basics.py", line 42, in <module>
    print(t[customer])
          ^
NameError: name 'customer' is not defined
```

1. **最后一行** = 异常类型 + 原因
2. **`^` 标记处** = 出错的那一列
3. **`line 42`** = 出错的行号

**最常见的 5 个错**：

| 报错 | 原因 | 改法 |
|---|---|---|
| `NameError: name 'x' is not defined` | 变量名拼错 / 忘了引号 | `t["customer"]` 不是 `t[customer]` |
| `IndentationError` | 缩进不一致 | 全用 4 空格，别用 Tab |
| `KeyError: 'xxx'` | 字典没这个键 | 改 `t.get("xxx", "")` |
| `TypeError: ... not subscriptable` | 类型不对 | 你可能对 str 用了 `[0]` |
| `ModuleNotFoundError` | 用错解释器 | 用 `.\scripts\py.cmd` 而不是 `python` |

**详细速查表**：`../../notes/python-cheatsheet.md`

---

## 写完了发朋友圈

```powershell
git add .
git commit -m "feat(py-01): 完成客服工单处理器 Step1+Step2"
git push
```

**这个提交会出现在你的 GitHub 主页上。** 3 个月的转行路上，这是面试官唯一能看到的证据链。

---

## 下一步

**Step 3 · 类与面向对象**（还没写，明天做）

把上面所有逻辑封装成一个 `Ticket` 类和 `TicketProcessor` 类——
这就是你未来主项目「AI 客服 Agent」的雏形结构。

预告：Step 3 的验收标准是**"能手写一个读写 JSON 的类"**，
正是 ROADMAP 里今天（10/22）定的产出物。

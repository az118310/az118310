# Python 关卡 · 零基础到能写项目

> **为什么重做了**：第一版作业一晚上塞了 8 个新概念（`**kwargs`、类型注解、推导式、`with`、`json`、异常处理…），
> 零基础看第二关直接懵。这不是你的问题，是坡度设计失败。
> 这一版拆成 5 关，每关只教 1-2 个语法点，从「不用碰文件、不用碰 JSON」开始。

---

## 怎么用

```powershell
cd D:\app\2026-10-21-21-42-36\agent-learning

# 1. 打开关卡文件，把 ___ 换成你的答案
#    （文件在 levels/ 目录，每关一个 .py）

# 2. 跑一关
.\scripts\py.cmd projects\py-01\levels\L1_variables.py

#    没填完时它会告诉你哪几行没填，不会让你看一堆看不懂的报错

# 3. 全部填完后自动批改
.\scripts\py.cmd projects\py-01\levels\check.py
```

**卡住超过 20 分钟**：看文件末尾的【答案】区，或者 `levels/solution/` 下有完整版。

---

## 5 关地图

| 关卡 | 文件 | 语法点 | 题数 | 你的真实场景 |
|---|---|---|---|---|
| **L1** | `L1_variables.py` | 变量、字符串、数字、f-string、注释、类型转换 | 8 | 给客户回话术，拼句子 |
| **L2** | `L2_strings.py` | 字符串方法：len/切片/in/replace/split/strip/endswith/find | 12 | 从商品标题里抠款号、颜色、面料 |
| **L3** | `L3_lists.py` | 列表：创建/索引/切片/遍历/推导式/append/max | 9 | 处理工单列表，筛出高优先级 |
| **L4** | `L4_dicts.py` | 字典：取值/get/in/items/修改/**字典计数器** | 11 | 单条工单的结构化存取 |
| **L5** | `L5_conditions.py` | if/elif/else、and/or/not、break/continue | 6 | 工单自动分流 |

**建议节奏**：一天一关。每关 30-40 分钟。**不要跳关。**

---

## 每关的三个动作

**1. 先猜。** 每一题上面都有【先猜】——先在脑子里或纸上猜输出是什么。
这个动作比直接看答案重要 10 倍。猜错了，你才知道自己哪里理解偏了。

**2. 再填。** `___` 是占位符。把它换成你的答案。

**3. 跑。** 跑完对照【先猜】看对不对。

---

## 三种填空标记

| 标记 | 长什么样 | 你要做什么 |
|---|---|---|
| `___` | `price = ___` | 填一个值/表达式 |
| `{___}` | `print(f"{___}")` | 填一个值，会被打印出来 |
| `# TODO 5-x：` | `if price < 100:  # TODO 5-1：把这个 100 改成…` | 这行代码已经写好，按注释要求改 |

**L5 用的是第三种**——因为运算符位置不能填 `___`（`if price ___ 100` 是语法错误）。
所以 L5 的题目是「看懂这段代码在干嘛，然后按要求微调」，而不是从零写。

---

## 遇到报错怎么办

**三步定位法**（报错信息从下往上读）：

```
Traceback (most recent call last):
  File "L1_variables.py", line 82, in <module>
    print(f"转换后加 1：{price_text + 1}")
                         ^^^^^^^^^^^^
TypeError: can only concatenate str (not "int") to str
```

1. **最后一行** = 异常类型 + 原因
2. **`^` 标记处** = 出错的那一列
3. **`line 82`** = 出错的行号

**最常见的 5 个**：

| 报错 | 原因 | 改法 |
|---|---|---|
| `NameError: name 'x' is not defined` | 变量名拼错 / 忘了引号 | `t["customer"]` 不是 `t[customer]` |
| `IndentationError` | 缩进不一致 | 全用 4 空格，别用 Tab |
| `TypeError: ... not subscriptable` | 类型不对 | 字符串也能 `[0]`，但那取的是字符不是字典键 |
| `KeyError: 'xxx'` | 字典没这个键 | 改用 `.get("xxx", "")` |
| `SyntaxError: invalid syntax` | 语法写错 | 看 `^` 指的位置 |

**完整速查表**：`../../notes/python-cheatsheet.md`

---

## 通关之后

L5 通关，你就具备了写 **L6 函数 + L7 文件读写 + L8 类** 的基础。

这三关合起来，就是你 ROADMAP 里 10/22 定的产出物：**「能手写一个读写 JSON 的类」**。

写完这 8 关，你会具备的能力：
- 独立看懂并修改一段中等复杂度的 Python 代码
- 把业务需求翻译成代码（筛选、计数、分流、统计）
- 这正是 AI 应用开发岗位 JD 里「Python 熟练」的实际含义

---

## 文件说明

```
levels/
├── L1_variables.py      ← 你的作业（骨架，有 ___ 和 TODO 标记）
├── L2_strings.py
├── L3_lists.py
├── L4_dicts.py
├── L5_conditions.py
├── guard.py             ← 占位符检查器（别改）
├── check.py             ← 自动批改
├── generate.py          ← 骨架/答案生成器（别改）
└── solution/            ← 标准答案（卡住再看）
    ├── L1_solution.py
    └── ...
```

**为什么要用生成器**：骨架和答案必须逐字对应。手工维护两份文件早晚会不一致
（开发这套东西时已经踩了三次）。改题目请改 `generate.py` 然后重新运行它。

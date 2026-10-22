# py-01 · Python 从零到能写项目

> **目标**：不学语法大全，做一个你每天都在干的事——处理客服工单。
> 做完你会真的写 Python 了，不是"看懂了"。

---

## 当前状态

**学习入口在 `levels/` 目录**（新拆的 5 关，零基础起步）。
`levels/README.md` 是详细说明。

---

## 快速开始

```powershell
cd D:\app\2026-10-21-21-42-36\agent-learning

# 跑第 1 关（没填完会告诉你哪几行没填）
.\scripts\py.cmd projects\py-01\levels\L1_variables.py

# 全部填完后自动批改
.\scripts\py.cmd projects\py-01\levels\check.py
```

---

## 目录

```
py-01/
├── levels/                  ← 学习入口（先看 levels/README.md）
│   ├── L1_variables.py      变量/字符串/数字
│   ├── L2_strings.py        字符串方法
│   ├── L3_lists.py          列表
│   ├── L4_dicts.py          字典
│   ├── L5_conditions.py     条件与循环控制
│   ├── guard.py             占位符检查器
│   ├── check.py             自动批改
│   ├── generate.py          骨架/答案生成器
│   └── solution/            标准答案
├── data/
│   └── tickets.json         10 条模拟客服工单（L6+ 用）
└── _archived_v1/            第一版作业（坡度太陡，已废弃，勿做）
```

---

## 通关标准

5 关全部批改 PASS，然后进入：
- **L6 函数**（把逻辑打包复用）
- **L7 文件读写 + JSON**（读 tickets.json、写日报）
- **L8 类**（把工单封装成 Ticket 类）

这三关合起来 = ROADMAP 里 10/22 定的产出物：**「能手写一个读写 JSON 的类」**。

---

## 写完了提交

```powershell
git add .
git commit -m "feat(py-01): 完成 Python 关卡 L1-L5"
git push
```

**这个提交会出现在你的 GitHub 主页上。** 3 个月后面试官点开看到的，就是这条轨迹。

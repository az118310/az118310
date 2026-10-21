# 今晚就做：Day 0 启动清单（10/21 晚间，30-45 分钟）

按顺序做，每步都有验收。做完了明天就有基础了。

---

## 步骤 1 · 建工作区并初始化 Git（10 分钟）

```bash
cd D:/app/2026-10-21-21-42-36/agent-learning
git init
git add .
git commit -m "chore: 初始化 AI 开发学习工作区"
```

验收：`git log` 能看到一条提交

## 步骤 2 · 确认 Python 环境（5 分钟）

环境已经装好了（隔离在 `~/.workbuddy/binaries/python/envs/default`），验证一下：

```bash
"C:/Users/Lee/.workbuddy/binaries/python/envs/default/Scripts/python.exe" -c "import mcp, openai; print('mcp', mcp.__file__); print('openai OK')"
```

已装好：`mcp 2.3.0`、`openai 3.35.1`

**但你自己平时用 `python` 命令可能指向系统 Python。** 建议在项目里放一个 `activate.bat`（Windows）或直接在 VSCode 里选解释器。

VSCode 里：`Ctrl+Shift+P` → `Python: Select Interpreter` → 选
`C:\Users\Lee\.workbuddy\binaries\python\envs\default\Scripts\python.exe`

## 步骤 3 · 装 VSCode + Python 扩展（10 分钟）

如果已有就跳过。扩展面板搜 `Python` 装微软官方那个，然后 `Ctrl+Shift+P` → `Python: Create Environment` → Venv。

## 步骤 4 · 跑通第一个脚本（10 分钟）

```bash
cd D:/app/2026-10-21-21-42-36/agent-learning/projects/mcp-01
"C:/Users/Lee/.workbuddy/binaries/python/envs/default/Scripts/python.exe" server.py --test
```

预期看到三个工具的测试输出。**这一步不消耗任何 API 额度，纯本地。**

## 步骤 5 · 申请一个 LLM API Key（15 分钟）

推荐 DeepSeek（便宜、兼容 OpenAI SDK、国内直连）：
- 官网 `platform.deepseek.com` → 注册 → 充值（最低几十块够你练到明年 1 月）
- 创建 API Key

拿到后设置环境变量（Git Bash）：
```bash
export OPENAI_API_KEY=sk-xxxxxxxx
```

或者直接写进项目里的 `.env`（记得加 `.gitignore`，**千万别把 key 提交到 GitHub**）

## 步骤 6 · 跑通第一次 LLM 调用（10 分钟）

```bash
cd D:/app/2026-10-21-21-42-36/agent-learning/projects/llm-01
"C:/Users/Lee/.workbuddy/binaries/python/envs/default/Scripts/python.exe" basic_call.py
```

**预期看到模型回复 + token 用量。** 这一刻你就正式入门了。

---

## 完成后（明天 10/22）

明天晚间的任务是 **Python 语法速成**。先做这个热身（30 分钟就够）：

创建 `projects/skill-01/exercise.py`，写一个函数：
- 输入：一句客户留言
- 输出：判断该回复"好"还是"差"，并打印

然后故意写错 3 次，练习看报错信息。

---

## 今天不用做的事（别贪多）

- ❌ 不用注册一堆课程平台
- ❌ 不用看 GitHub 上别人的 AI 项目（会掉进收藏陷阱）
- ❌ 不用纠结"到底学 LangChain 还是 LlamaIndex"（11/09 再说）
- ❌ 不用买课

---

## 一句话总结今天

> 环境已就绪，MCP SDK 和 openai SDK 都装好了，代码模板全部验证可跑。
> 今晚只做一件事：**把 LLM API Key 搞到手，跑通 `basic_call.py`。**
> 剩下的 10 个月，慢慢来。

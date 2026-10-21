# 今晚就做：Day 0 启动清单（10/21 晚间，30-45 分钟）

按顺序做，每步都有验收。做完了明天就有基础了。

> **环境已全部帮你配好**（10/21 23:00 更新）
> Git ✅ · Python 3.13 ✅ · mcp 2.3.0 / openai 3.35.1 / anthropic 1.17.0 ✅
> GitHub SSH 认证 ✅ · 3 个提交已推送 ✅ · PowerShell 编码已修复 ✅
> **剩下唯一没做的：申请一个 LLM API Key。**

---

## 步骤 1 · 验证环境（2 分钟）

关掉当前 PowerShell，**新开一个窗口**（PATH 和编码配置只对新窗口生效），然后：

```powershell
cd D:\app\2026-10-21-21-42-36\agent-learning
.\scripts\check_env.ps1
```

预期输出：全绿（`[ OK ]`），只有 LLM API Key 那一项是 `[WARN]`（因为还没申请）。

**这就是以后每天的自检命令**，一条命令看全部状态。

顺手验证 Git 推��已经通了：
```powershell
git log --oneline
```
预期看到 4 条提交，最新一条是 `feat: 新增 PowerShell 快捷脚本与速查表...`

---

## 步骤 2 · 申请 LLM API Key（15 分钟）

**推荐 DeepSeek**（国内直连、兼容 OpenAI SDK、新用户有赠送额度）：
- 打开 `https://platform.deepseek.com/api_keys` → 注册 → 创建 API Key
- 新用户通常有赠送额度，不充值也能先跑通

备选（都有免费额度）：
| 服务商 | 申请地址 | 说明 |
|---|---|---|
| 通义千问 | `https://bailian.console.aliyun.com/` | 新用户 100 万 tokens 免费 |
| 智谱 GLM | `https://open.bigmodel.cn/usercenter/apikeys` | `glm-4-flash` 可无限量调用 |

拿到 Key 后，用现成脚本写进配置文件（**不会打印你的 Key，不会提交到 GitHub**）：

```powershell
.\scripts\py.cmd scripts\setup_key.py --interactive
```

它会引导你选服务商、粘贴 Key，自动写入 `.env`。

---

## 步骤 3 · 跑通第一次 LLM 调用（5 分钟）

```powershell
.\scripts\py.cmd projects\llm-01\basic_call.py
```

**预期看到模型回复 + token 用量。** 这一刻你就正式入门了。

如果报 401，按这个顺序查：
1. Key 是否复制完整（别带空格）
2. 账户是否有余额（DeepSeek 新账号赠送额度可能需要手动激活）
3. 换服务商试（千问/智谱的申请和调用方式一样）

---

## 步骤 4 · 顺手玩一下 MCP Server（5 分钟）

**这一步不消耗任何 API 额度，纯本地。**

```powershell
.\scripts\py.cmd projects\mcp-01\server.py --test
```

预期看到 `query_order`、`track_logistics`、`get_presale_schedule` 三个工具的测试输出，
包括"查不到就明确报错不编造"那个分支。

---

## 步骤 5 · 提交你的第一个代码（5 分钟）

```powershell
git add .
git commit -m "feat: 配置 LLM API Key，跑通首次模型调用"
git push
```

**这三条命令就是你求职时展示学习轨迹的方式。** commit message 认真写——
面试官会点开你的 GitHub 看提交记录，别写"test""fix bug"这种。

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

> 环境已就绪，代码模板全部验证可跑，GitHub 已连通。
> 今晚只做一件事：**申请 API Key，跑通 `basic_call.py`。**
> 剩下的 10 个月，慢慢来。

---

## 附：常用命令速查

```powershell
# 环境自检
.\scripts\check_env.ps1

# 跑 Python 脚本
.\scripts\py.cmd projects\llm-01\basic_call.py
.\scripts\py.cmd -c "import mcp; print(mcp.__version__)"

# Git 三件套
git add .
git commit -m "feat: xxx"
git push

# 配置 API Key
.\scripts\py.cmd scripts\setup_key.py --interactive
```

**PowerShell 报错看不懂时**，翻 `plan/POWERSHELL-CHEATSHEET.md`，
那里记了 6 个你今天实际撞过的坑和对应解法。

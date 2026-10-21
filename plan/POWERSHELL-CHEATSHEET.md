# PowerShell 速查表（新手向）

写这份是因为 10/21 这一天你连续撞了 4 个 PowerShell 特有的坑。
每个都给出**错误信息 → 真实原因 → 正确写法**。

---

## 坑 1 · 引号开头的路径不是命令

### 错误
```powershell
"C:/Users/Lee/.workbuddy/binaries/python/envs/default/Scripts/python.exe" -c "import mcp"
```
```
表达式或语句中包含意外的标记“-c”。
```

### 原因
PowerShell 把 `"C:/..."` 解析成**字符串表达式**（一个没被使用的值），
然后 `-c` 就成了无法解析的语法。Bash 不这样，Bash 会把它当命令。

### 正确写法（三种任选）
```powershell
# A. 调用运算符 &（最标准）
& "C:/Users/Lee/.workbuddy/binaries/python/envs/default/Scripts/python.exe" -c "import mcp"

# B. 用本项目封装好的快捷脚本（推荐，最省事）
.\scripts\py.cmd -c "import mcp; print(mcp.__version__)"
.\scripts\py.cmd projects\llm-01\basic_call.py

# C. 临时改当前会话的 PATH，之后直接写 python
$env:Path = "$env:USERPROFILE\.workbuddy\binaries\python\envs\default\Scripts;$env:Path"
python -c "import mcp"
```

**记忆点：PowerShell 里凡是要执行一个带引号路径的东西，前面加 `&`。**

---

## 坑 2 · 执行策略禁止运行 .ps1

### 错误
```powershell
.\scripts\check_env.ps1
```
```
无法加载文件 ...，因为在此系统上禁止运行脚本。
```
```
FullyQualifiedErrorId : UnauthorizedAccess
```

### 原因
Windows 默认的 `ExecutionPolicy` 是 `Restricted`，禁止运行任何脚本。

### 解决（已在本机配置好）
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

- `CurrentUser` 作用域：**不需要管理员权限**，只影响你的账户
- `RemoteSigned` 含义：本地自己写的脚本可以跑，从网上下载的必须带数字签名
- 这是微软官方推荐给开发者的设置，不会降低系统安全等级

**验证已生效**：`Get-ExecutionPolicy -Scope CurrentUser` → `RemoteSigned`

### 只想临时跑一次（不修改设置）
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check_env.ps1
```

---

## 坑 3 · UTF-8 脚本中文乱码 → 语法错误

### 错误
```
字符串缺少终止符: "。
语句块或类型定义中缺少右“}”。
```
看起来像脚本写错了，其实是**编码问题**。

### 原因
PowerShell 5.1（Windows 自带的那个）读取 `.ps1` 时：
- 有 BOM → 正确识别为 UTF-8，中文正常
- **无 BOM → 按 ANSI/GBK 解析**，中文字符的字节被拆坏，
  引号识别失败 → 报"缺少终止符"这种看起来毫不相关的错

### 解决
**给 `.ps1` 文件加 UTF-8 BOM。** 用编辑器（VS Code）存为 `UTF-8 with BOM`，
或者用脚本批量处理：

```bash
python -c "
p='check_env.ps1'
d=open(p,'rb').read()
if not d.startswith(b'\xef\xbb\xbf'):
    open(p,'wb').write(b'\xef\xbb\xbf'+d)
"
```

> 本项目的 `scripts/check_env.ps1` 已经带好 BOM，你直接改内容时如果用
> Write 工具覆盖，**记得重新加一次 BOM**，否则会重现这个错。

---

## 坑 4 · .cmd 脚本需要 CRLF 换行

### 原因
`.cmd` / `.bat` 是给 Windows 命令解释器用的，它按 **CRLF** 切分命令。
如果文件是纯 LF，某些情况下命令会被粘成一行导致解析失败。

### 解决
```bash
python -c "
raw=open('py.cmd','rb').read().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
open('py.cmd','wb').write(raw)
"
```

> `scripts/py.cmd` 已经是 CRLF。

---

## 坑 5 · PATH 改了但当前窗口没生效

### 现象
已经 `[Environment]::SetEnvironmentVariable("Path", ..., "User")` 写进去了，
但当前窗口还是 `git 不是内部或外部命令`。

### 原因
Windows 环境变量**在进程启动时快照一次**。新 PATH 只对新开的窗口有效。

### 解决
**关掉当前终端，重开一个。** 不想重开的话，在当前窗口临时生效：

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
```

> `scripts/check_env.ps1` 开头已经内置了这段，所以它永远能找到 git。

---

## 坑 6 · 复制粘贴的换行变成了 `^X` / `X`

### 现象
从网页或聊天窗口复制多行命令到 PowerShell，换行变成了 `X`，
或者命令被合并成一行。

### 原因
PowerShell 5.1 的控制台在某些渲染路径下会把回车显示成 `X`。
如果真粘进终端了，命令会变成 `irmhttps://...` 这种连在一起的东西。

### 解决
- **终端里执行**（不是脚本里）：一行一行敲，别整段粘
- **写进 `.ps1` 里**：正常保存即可（BOM + CRLF）
- 怀疑出问题时：先 `Write-Host` 把变量打出来看实际值

---

## 常用命令速查

```powershell
# 目录
cd D:\app\2026-10-21-21-42-36\agent-learning
ls                      # 列出
pwd                     # 当前目录

# Git（PATH 已配好，新窗口直接用）
git status
git add .
git commit -m "feat: xxx"
git push
git log --oneline

# Python（用快捷脚本）
.\scripts\py.cmd projects\llm-01\basic_call.py
.\scripts\py.cmd -c "import mcp; print(mcp.__version__)"

# 环境自检（一条命令看全部状态）
.\scripts\check_env.ps1

# 执行策略
Get-ExecutionPolicy -Scope CurrentUser
```

---

## 和 Bash 的关键差异（最容易搞混的地方）

| 操作 | Bash (Git Bash) | PowerShell |
|---|---|---|
| 执行带引号路径 | `"C:/path/x.exe" -c "..."` 直接可跑 | 必须加 `&` 前缀 |
| 环境变量 | `export A=1` | `$env:A = "1"` |
| 读环境变量 | `$A` | `$env:A` |
| 变量 | `x=1` | `$x = 1` |
| 管道给命令 | `cat f \| cmd` | `cmd < f`（注意方向相反） |
| 链式执行 | `a && b` | `a; b`（`&&` 需 PowerShell 7+） |
| 后台 | `cmd &` | `Start-Job`（本机被安全策略拦） |
| 脚本参数 | `$1` | `$args[0]` 或 `param()` |
| 引号转义 | `\"` | `` `" `` 或 `''` |

**建议：学习阶段用 PowerShell 做"日常操作"，写代码用编辑器/VS Code。**
两个 Shell 的差异会持续消耗你的注意力，不值得在转行期硬扛。

# 把代码推送到 GitHub —— 最后一步（需你手动操作，3 分钟）

## 现状（我已全部搞定）

| 项目 | 状态 |
|---|---|
| Git 可执行文件 | ✅ 已装并进 PATH |
| 全局身份 | ✅ `Lee <lee@workbuddy.local>` |
| 本地仓库 | ✅ 已初始化，2 个提交在 master 分支 |
| remote 地址 | ✅ `git@github.com:az118310/az118310.git`（SSH over 443） |
| SSH 密钥 | ✅ 已生成：`~/.ssh/id_ed25519_github` |
| SSH 通道 | ✅ 已验证连通（握手成功到 GitHub 认证层） |
| GitHub 仓库 | ✅ `az118310/az118310` 存在且可访问 |
| OAuth 浏览器授权 | ❌ GitHub 的 device/code 端点当前 503，故改走 SSH |

**唯一剩下的事：把公钥加到 GitHub 账号。**

---

## 第 1 步：复制公钥

公钥内容（整行复制，别漏空格）：

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPP/ynd9KK2+7BHY5HN1O8XHg7AZ2Q3gCFRFDSc3rjZt az118310@github
```

或者在 PowerShell 里执行这一行直接复制到剪贴板：

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519_github.pub" | Set-Clipboard
```

## 第 2 步：添加到 GitHub

1. 打开 **https://github.com/settings/ssh/new**
   - 如果打不开，改用镜像：https://gitclone.com/github.com/settings/ssh/new
2. 填写：
   - **Title**：`WorkBuddy-Lee`
   - **Key**：粘贴上面那一整行
   - **Authentication key**（可选）：留空
3. 点 **Add SSH key**（需要输入 GitHub 密码）

## 第 3 步：验证

在 PowerShell 执行：

```powershell
ssh -T git@github.com
```

**看到这行就算成功**（提示语里说"成功认证"，但不认仓库是正常的）：

```
Hi az118310! You've successfully authenticated, but GitHub does not provide shell access.
```

如果还是报 `Permission denied (publickey)`，说明公钥没保存成功，回第 2 步检查。

## 第 4 步：推送

```powershell
cd D:\app\2026-10-21-21-42-36\agent-learning
git push -u origin master
```

预期输出：

```
Enumerating objects: 9, done.
...
branch 'master' set up to track 'origin/master'.
```

## 第 5 步：确认

浏览器打开 **https://github.com/az118310/az118310**，应该能看到：
- `plan/` `projects/` `portfolio/` `notes/` `scripts/` 目录
- 2 条提交记录

---

## 以后怎么用

配置完一次，之后每次都是两条命令：

```powershell
git add .
git commit -m "描述你做了什么"
git push
```

**这三条命令就是你未来 3 个月学习轨迹的记录。** 面试官点开你的 GitHub，能看到从 10 月 21 日到明年 1 月的持续提交——这比任何课程证书都有说服力。

建议 commit message 格式（面试官会看）：

```
feat: 新增 RAG 混合检索模块
fix: 修复商品知识库查不到时的空指针
docs: 补充 LangChain 与 LlamaIndex 的选型对比
chore: 更新依赖版本
```

---

## 如果卡住了

| 现象 | 原因 | 解决 |
|---|---|---|
| `Permission denied (publickey)` | 公钥没加成功 | 重做第 2 步 |
| `ssh: Could not resolve hostname` | 用了 SSH 但 config 没生效 | 确认 `~/.ssh/config` 存在且内容正确 |
| `Connection timed out` | 走了 22 端口 | 确认 config 里 `Port 443` |
| 网页打不开 settings/ssh/new | 网络问题 | 用 https://gitclone.com/github.com/settings/ssh/new |
| `remote origin already exists` | remote 已存在 | 用 `git remote set-url origin <新地址>`，不要用 `add` |

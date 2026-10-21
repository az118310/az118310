$ErrorActionPreference = 'Continue'

# 刷新 PATH：读取系统级 + 用户级，写入当前进程
$machine = [Environment]::GetEnvironmentVariable('Path','Machine')
$user    = [Environment]::GetEnvironmentVariable('Path','User')
if ($machine -and $user) { $env:Path = "$machine;$user" }

$repo = "D:\app\2026-10-21-21-42-36\agent-learning"

$PyCandidates = @(
    "$env:USERPROFILE\.workbuddy\binaries\python\envs\default\Scripts\python.exe",
    "$env:USERPROFILE\.workbuddy\binaries\python\versions\3.13.12\python.exe"
)
$Py = $PyCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

function Section($t) {
    Write-Host ''
    Write-Host ('-- ' + $t + ' ' + ('-' * [Math]::Max(0, 46 - $t.Length)))
}

function Ok($m)   { Write-Host ('  [ OK ] ' + $m) -ForegroundColor Green }
function Warn($m) { Write-Host ('  [WARN] ' + $m) -ForegroundColor Yellow }
function Bad($m)  { Write-Host ('  [FAIL] ' + $m) -ForegroundColor Red }

Section 'Python 环境'
if ($Py) {
    Ok ("解释器: " + $Py)
    $ver = & $Py -c "import sys;print(sys.version.split()[0])"
    if ($ver) { Ok ("版本: " + ($ver -join ' ')) } else { Bad '解释器无法执行' }
} else {
    Bad '未找到隔离 Python 环境'
}

Section '关键依赖'
if ($Py) {
    foreach ($pkg in @('mcp','openai','anthropic')) {
        $v = & $Py -c "import $pkg;print(getattr($pkg,'__version__','ok'))" 2>$null
        if ($v) { Ok ("$pkg " + ($v -join ' ')) } else { Warn "$pkg 未安装" }
    }
}

Section 'Git'
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    Ok ("git -> " + $git.Source)
    Ok ((git --version) -join ' ')
} else {
    Bad 'git 不在 PATH'
}

Section 'GitHub 认证'
if (Test-Path $repo) {
    Push-Location $repo
    $remote = git remote -v 2>$null | Select-Object -First 1
    if ($remote) { Ok ('remote: ' + $remote) } else { Warn '尚未配置 remote' }
    $n = @(git log --oneline 2>$null).Count
    Ok ("本地提交数: $n")
    $branch = git branch --show-current 2>$null
    $unpushed = @(git log --oneline "origin/$branch..HEAD" 2>$null).Count
    if ($unpushed -gt 0) { Warn ("有 $unpushed 个提交未推送到远端") } else { Ok '所有提交已同步到远端' }
    Pop-Location
} else {
    Warn '仓库目录未找到'
}

if (Test-Path "$env:USERPROFILE\.ssh\id_ed25519_github") {
    Ok 'SSH 私钥存在'
    $ssh = "$env:USERPROFILE\.workbuddy\binaries\PortableGit\current\usr\bin\ssh.exe"
    if (Test-Path $ssh) {
        $out = & $ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 -T git@github.com 2>&1
        $txt = ($out -join ' ')
        if ($txt -match 'successfully authenticated') { Ok 'GitHub SSH 认证成功' }
        elseif ($txt -match 'Permission denied') { Warn '公钥尚未添加到 GitHub -- 见 plan/GITHUB-SETUP.md' }
        else { Warn ('SSH 握手异常: ' + $txt) }
    }
} else {
    Warn '未生成 SSH 密钥'
}

Section '作品集文件'
foreach ($f in @('plan\ROADMAP.md','plan\DAY0-START.md','plan\GITHUB-SETUP.md','portfolio\README.md','projects\mcp-01\server.py','projects\llm-01\basic_call.py','projects\llm-02\tool_loop.py')) {
    if (Test-Path (Join-Path $repo $f)) { Ok $f } else { Warn "$f 缺失" }
}

Section 'LLM API Key'
$keyFile = Join-Path $repo '.env'
if (Test-Path $keyFile) {
    $raw = Get-Content $keyFile -Raw
    if ($raw -match 'sk-[A-Za-z0-9_\-]{10,}') { Ok '.env 中已配置 API Key' }
    else { Warn '.env 存在但未找到有效 Key' }
} else {
    Warn '尚未创建 .env -- 见 plan/DAY0-START.md 步骤 5'
}

Write-Host ''
Write-Host '自检结束。'

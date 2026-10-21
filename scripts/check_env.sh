#!/usr/bin/env bash
# 环境自检脚本 —— 随时运行，确认学习环境是否完好
# 用法: bash scripts/check_env.sh

echo "=============================================="
echo "  AI 开发学习环境自检"
echo "=============================================="

FAIL=0

# --- Git ---
echo ""
echo "[1] Git"
if command -v git >/dev/null 2>&1; then
    echo "  ✓ $(git --version)"
    echo "    路径: $(command -v git)"
    if [ -n "$(git config --global user.name)" ]; then
        echo "    身份: $(git config --global user.name) <$(git config --global user.email)>"
    else
        echo "    ✗ 未配置全局身份，执行: git config --global user.name \"你的名字\""
        FAIL=1
    fi
else
    echo "  ✗ git 不可用"
    echo "    修复: 新开一个终端窗口（PATH 变更需重启终端生效）"
    echo "    或手动加 PATH: C:\\Users\\Lee\\.workbuddy\\binaries\\PortableGit\\current\\cmd"
    FAIL=1
fi

# --- Git 远程与认证 ---
echo ""
echo "[1b] Git 远程与认证"
GIT_ROOT="D:/app/2026-10-21-21-42-36/agent-learning"
if [ -d "$GIT_ROOT/.git" ]; then
    echo "    remote: $(git -C "$GIT_ROOT" remote get-url origin 2>/dev/null || echo '未设置')"
    echo "    分支:   $(git -C "$GIT_ROOT" branch --show-current 2>/dev/null || echo '?')"
    echo "    提交数: $(git -C "$GIT_ROOT" rev-list --count HEAD 2>/dev/null || echo 0)"
    if [ -f "C:/Users/Lee/.ssh/id_ed25519_github.pub" ]; then
        echo "    ✓ SSH 密钥已生成"
    else
        echo "    ✗ SSH 密钥缺失"
        FAIL=1
    fi
    if [ -f "C:/Users/Lee/.ssh/config" ]; then
        echo "    ✓ SSH config 存在"
    else
        echo "    ✗ SSH config 缺失"
        FAIL=1
    fi
fi

# --- Python ---
echo ""
echo "[2] Python"
PY_WIN="C:/Users/Lee/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
if [ -f "$PY_WIN" ]; then
    echo "  ✓ 隔离环境存在"
    echo "    版本: $("$PY_WIN" --version 2>&1)"
    for pkg in mcp openai anthropic; do
        if "$PY_WIN" -c "import $pkg" 2>/dev/null; then
            echo "    ✓ $pkg"
        else
            echo "    ✗ $pkg 未安装"
            FAIL=1
        fi
    done
else
    echo "  ✗ 隔离环境不存在: $PY_WIN"
    FAIL=1
fi

# --- 项目文件 ---
echo ""
echo "[3] 项目文件"
ROOT="D:/app/2026-10-21-21-42-36/agent-learning"
for f in "plan/ROADMAP.md" "plan/DAY0-START.md" "portfolio/README.md" \
         "projects/llm-01/basic_call.py" "projects/llm-02/tool_loop.py" \
         "projects/mcp-01/server.py" "notes/DAILY-TEMPLATE.md" \
         "notes/WEEKLY-TEMPLATE.md"; do
    if [ -f "$ROOT/$f" ]; then
        echo "  ✓ $f"
    else
        echo "  ✗ $f 缺失"
        FAIL=1
    fi
done

# --- Skill ---
echo ""
echo "[4] 客服 Skill"
SKILL="C:/Users/Lee/.workbuddy/skills/taobao-qa"
if [ -f "$SKILL/SKILL.md" ]; then
    echo "  ✓ taobao-qa 已安装"
    if [ -f "$SKILL/scripts/kb_search.py" ]; then
        echo "    ✓ 检索脚本就位"
    else
        echo "    ✗ 检索脚本缺失"
        FAIL=1
    fi
else
    echo "  ✗ taobao-qa Skill 未安装"
    FAIL=1
fi

# --- API Key ---
echo ""
echo "[5] LLM API Key"
if [ -n "$OPENAI_API_KEY" ]; then
    echo "  ✓ 已设置 (当前 shell)"
else
    echo "  ⚠ 当前 shell 未设置 OPENAI_API_KEY"
    echo "    这不影响其他功能，只是跑 LLM 脚本前需要设置"
fi

echo ""
echo "=============================================="
if [ $FAIL -eq 0 ]; then
    echo "  结果: 全部通过 ✓"
else
    echo "  结果: 有项目需要修复（见上方 ✗ 标记）"
fi
echo "=============================================="

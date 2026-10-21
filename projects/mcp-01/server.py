#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""订单查询 MCP Server —— Day 5-6 (11/24) 晚间主任务

教学目标: 理解 MCP Server 的三个要素
    1. Tool 定义 —— 告诉模型「有哪些工具、参数长什么样」
    2. Tool 实现 —— 模型调用时真正执行的函数
    3. Transport —— stdio (本地进程) / sse / streamable-http (远程服务)

版本兼容说明:
    MCP 官方 SDK 在 2.x 把 FastMCP 改名成 MCPServer, 本文件自动兼容:
        mcp >= 2.0  -> from mcp.server.mcpserver import MCPServer
        mcp <  2.0  -> from mcp.server.fastmcp import FastMCP
    装新版用:  pip install -U mcp
    装旧版用:  pip install "mcp<2"

运行:
    python server.py            # stdio 模式, 供 MCP 客户端连接
    python server.py --test     # 自测模式, 不需要客户端

接入 WorkBuddy:
    1) 把本文件路径填进 ~/.workbuddy/mcp.json 的 mcpServers
    2) 重启 WorkBuddy, 输入 /mcp 查看连接状态
    3) 对话中直接问「查一下订单 20241031001」即可触发
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Any

# ------------------------------------------------------------------
# 版本自适应导入
# ------------------------------------------------------------------
try:
    from mcp.server.mcpserver import MCPServer  # MCP >= 2.0
    _SDK = "2.x"
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer  # MCP < 2.0
        _SDK = "1.x"
    except ImportError:
        print("未安装 MCP SDK。请执行: pip install -U mcp", file=sys.stderr)
        sys.exit(1)


# ------------------------------------------------------------------
# 初始化
# ------------------------------------------------------------------
# MCPServer 会自动从 docstring 生成 Tool 的 description 和参数 schema,
# 所以下面的 docstring 不是注释, 是模型「看到」的说明 —— 写清楚很重要。
mcp = MCPServer(
    name="order-service",
    instructions="淘宝订单与物流查询服务。用于回答客户关于订单状态、发货时间、物流轨迹、预售排期的问题。",
)

# 模拟数据库: 生产环境这里换成真实查询
FAKE_ORDERS: dict[str, dict[str, Any]] = {
    "20241031001": {
        "order_id": "20241031001",
        "status": "已发货",
        "product": "法式复古碎花连衣裙",
        "size": "M",
        "color": "雾霾蓝",
        "amount": 189.00,
        "ship_from": "浙江杭州",
        "ship_time": "2026-10-29 16:20",
        "tracking_no": "SF1234567890",
        "buyer_note": "",
    },
    "20241031002": {
        "order_id": "20241031002",
        "status": "待发货",
        "product": "简约陶瓷马克杯 400ml",
        "size": "标准",
        "color": "奶白",
        "amount": 49.00,
        "ship_from": "广东佛山",
        "ship_time": None,
        "tracking_no": "",
        "buyer_note": "麻烦帮忙包一下礼品，送人的",
    },
}


# ------------------------------------------------------------------
# Tool 1: 查询订单
# ------------------------------------------------------------------
@mcp.tool()
def query_order(order_id: str) -> dict:
    """查询淘宝订单的当前状态、物流和商品信息。

    Args:
        order_id: 订单编号, 形如 20241031001 的纯数字字符串。

    Returns:
        包含订单状态、发货时间、物流单号的字典。订单不存在时返回 error 字段。
    """
    order_id = order_id.strip()
    order = FAKE_ORDERS.get(order_id)

    if order is None:
        # 重要: 查不到就明确报错, 不要返回猜测内容
        return {
            "found": False,
            "error": f"未找到订单 {order_id}",
            "available_orders": list(FAKE_ORDERS.keys()),
        }

    result = dict(order)
    result["found"] = True

    # 已发货时, 估算一个到达时间 (演示真实场景下的派生逻辑)
    if order["ship_time"]:
        ship_dt = datetime.strptime(order["ship_time"], "%Y-%m-%d %H:%M")
        eta = ship_dt + timedelta(days=2)
        result["estimated_arrival"] = eta.strftime("%Y-%m-%d")
    else:
        result["estimated_arrival"] = None
        result["reminder"] = "该订单尚未发货, 请勿向客户承诺具体到货日期"

    return result


# ------------------------------------------------------------------
# Tool 2: 查询物流轨迹
# ------------------------------------------------------------------
@mcp.tool()
def track_logistics(tracking_no: str) -> dict:
    """根据物流单号查询最新一条物流轨迹。

    Args:
        tracking_no: 物流单号, 通常是 SF 开头加 10 位数字。

    Returns:
        最新轨迹和预计送达日期。查不到时返回 error 字段。
    """
    tracking_no = tracking_no.strip().upper()
    if not tracking_no.startswith("SF") or len(tracking_no) < 8:
        return {"found": False, "error": f"物流单号格式不正确: {tracking_no}"}

    for order in FAKE_ORDERS.values():
        if order["tracking_no"].upper() == tracking_no:
            ship_dt = (
                datetime.strptime(order["ship_time"], "%Y-%m-%d %H:%M")
                if order["ship_time"]
                else datetime.now()
            )
            return {
                "found": True,
                "tracking_no": tracking_no,
                "carrier": "顺丰速运",
                "latest_trace": f"【已揽收】{order['ship_from']} 顺丰速运 已揽收, 等待发出",
                "trace_time": ship_dt.strftime("%Y-%m-%d %H:%M"),
                "estimated_delivery": (ship_dt + timedelta(days=2)).strftime("%Y-%m-%d"),
                "status": order["status"],
            }

    return {"found": False, "error": f"未找到物流单号 {tracking_no} 的轨迹"}


# ------------------------------------------------------------------
# Tool 3: 预售排期
# ------------------------------------------------------------------
@mcp.tool()
def get_presale_schedule(product_name: str) -> dict:
    """查询某商品的预售批次和截单时间。

    Args:
        product_name: 商品名称关键字, 支持部分匹配。

    Returns:
        预售批次信息。非预售商品返回 not_presale 标记。
    """
    product_name = product_name.strip()
    presales = {
        "法式复古碎花连衣裙": {
            "batch": "2026 秋冬新款 第 3 批",
            "order_deadline": "2026-11-05 23:59",
            "expected_ship": "截单后 7 个工作日内",
            "presale_price": "169.00",
            "deposit": "定金 30 元, 尾款发货前支付",
        }
    }
    for name, info in presales.items():
        if product_name in name or name in product_name:
            return {"found": True, "product": name, "is_presale": True, **info}
    return {
        "found": True,
        "product": product_name,
        "is_presale": False,
        "message": "该商品非预售, 可直接下单, 按常规时效发货",
    }


# ------------------------------------------------------------------
# 自测: 不接客户端也能验证逻辑
# ------------------------------------------------------------------
def self_test() -> None:
    print("=" * 60)
    print(f"订单查询 MCP Server —— 自测 (MCP SDK {_SDK})")
    print("=" * 60)

    cases = [
        ("query_order 正常", lambda: query_order("20241031001")),
        ("query_order 不存在", lambda: query_order("99999999999")),
        ("track_logistics 正常", lambda: track_logistics("SF1234567890")),
        ("track_logistics 格式错", lambda: track_logistics("123")),
        ("get_presale 预售", lambda: get_presale_schedule("连衣裙")),
        ("get_presale 非预售", lambda: get_presale_schedule("马克杯")),
    ]

    for name, fn in cases:
        print(f"\n--- {name} ---")
        print(json.dumps(fn(), ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print("自测完成。接入客户端: python server.py")
    print("=" * 60)


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test()
    else:
        # stdio 传输: MCP 客户端通过 stdin/stdout 与本进程通信
        # 关键: 绝不能往 stdout 打印调试信息, 否则会破坏 JSON-RPC 协议流
        # 要打印就打到 stderr
        print("order-service MCP server 启动于 stdio, 等待客户端连接...", file=sys.stderr)
        mcp.run(transport="stdio")

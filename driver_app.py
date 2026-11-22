"""
RideGo 司机端 - Pi Network 生态打车应用
独立部署的司机端应用
"""

import streamlit as st
import time
from datetime import datetime

# ============ Pi Network 配置 ============
PI_API_URL = "https://api.testnet.minepi.com"  # 上线切换 mainnet
APP_ID = "ridego-driver"

# ============ 页面配置 ============
st.set_page_config(
    page_title="RideGo 司机端",
    page_icon="🚕",
    layout="wide"
)

# ============ 初始化会话状态 ============
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'driver' not in st.session_state:
    st.session_state.driver = None
if 'earnings' not in st.session_state:
    st.session_state.earnings = 0.0

# ============ 主界面 ============
st.title("🚕 RideGo 司机端")
st.markdown("---")

# 登录区域
with st.sidebar:
    st.header("👨✈️ 司机登录")
    username = st.text_input("司机姓名")
    wallet = st.text_input("Pi 钱包地址")
    plate = st.text_input("车牌号")
    car_model = st.text_input("车型")

    if st.button("登录并上线", type="primary", use_container_width=True):
        if username and wallet and plate:
            st.session_state.driver = {
                "name": username,
                "wallet": wallet,
                "plate": plate,
                "car_model": car_model,
                "status": "online",
                "rating": 5.0,
                "trips": 0
            }
            st.success(f"欢迎，{username}师傅！已上线")
        else:
            st.error("请填写司机姓名、钱包地址和车牌号")

    st.markdown("---")
    st.caption(f"网络: Testnet | App: {APP_ID}")

# 主内容区
if 'driver' not in st.session_state or st.session_state.driver is None:
    st.info("👈 请先在左侧登录并上线")
else:
    driver = st.session_state.driver

    # 司机信息卡片
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("状态", "🟢 在线" if driver["status"] == "online" else "🔴 离线")
    col2.metric("评分", f"⭐ {driver['rating']}")
    col3.metric("完成订单", driver["trips"])
    col4.metric("今日收入", f"{st.session_state.earnings} Pi")

    st.markdown("---")

    # 接单大厅
    st.subheader("📢 接单大厅")

    # 模拟待接订单（实际版从后端 API 获取）
    pending_orders = [
        {
            "id": "ORD001",
            "pickup": "江南水岸七组团",
            "destination": "重庆北站",
            "price": 12.5,
            "distance": 15,
            "passenger": "乘客A"
        },
        {
            "id": "ORD002",
            "pickup": "南坪万达广场",
            "destination": "解放碑",
            "price": 8.0,
            "distance": 8,
            "passenger": "乘客B"
        },
        {
            "id": "ORD003",
            "pickup": "重庆大学",
            "destination": "江北机场",
            "price": 25.0,
            "distance": 30,
            "passenger": "乘客C"
        }
    ]

    for order in pending_orders:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**订单号：{order['id']}**")
                st.write(f"📍 {order['pickup']} → 🏁 {order['destination']}")
                st.write(f"💰 {order['price']} Pi | 📏 {order['distance']}公里 | 👤 {order['passenger']}")
            with col2:
                if st.button(f"接单", key=f"accept_{order['id']}", type="primary"):
                    st.session_state.current_order = order
                    driver["status"] = "busy"
                    st.success(f"✅ 已接单 {order['id']}！")
                    st.rerun()

    # 当前行程
    if 'current_order' in st.session_state and st.session_state.current_order:
        st.markdown("---")
        st.subheader("🚗 当前行程")
        order = st.session_state.current_order

        with st.container(border=True):
            st.write(f"**订单号：{order['id']}**")
            st.write(f"📍 {order['pickup']} → 🏁 {order['destination']}")
            st.write(f"💰 {order['price']} Pi | 👤 {order['passenger']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🟢 已到达上车点", use_container_width=True):
                    st.info("等待乘客上车...")
            with col2:
                if st.button("✅ 完成订单", type="primary", use_container_width=True):
                    st.session_state.earnings += order["price"]
                    driver["trips"] += 1
                    driver["status"] = "online"
                    st.session_state.current_order = None
                    st.success(f"🎉 订单完成！收入 {order['price']} Pi 已到账")
                    st.rerun()

st.markdown("---")
st.caption("RideGo 司机端 v1.0 | Powered by Pi Network")

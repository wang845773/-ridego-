"""
RideGo 乘客端 - Pi Network 生态打车应用
独立部署的乘客端应用
"""

import streamlit as st
import uuid
import time
from datetime import datetime

# ============ Pi Network 配置 ============
PI_API_URL = "https://api.testnet.minepi.com"  # 上线切换 mainnet
APP_ID = "ridego-passenger"

# ============ 页面配置 ============
st.set_page_config(
    page_title="RideGo 乘客端",
    page_icon="🚗",
    layout="wide"
)

# ============ 初始化会话状态 ============
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'current_order' not in st.session_state:
    st.session_state.current_order = None

# ============ 价格计算 ============
def calculate_price(distance_km, car_type):
    """基于 Pi 的价格计算"""
    base = {"economy": 1.0, "comfort": 1.5, "premium": 2.5}
    per_km = {"economy": 0.5, "comfort": 0.8, "premium": 1.2}
    return round(base.get(car_type, 1.0) + distance_km * per_km.get(car_type, 0.5), 2)

# ============ 主界面 ============
st.title("🚗 RideGo 乘客端")
st.markdown("---")

# 登录区域
with st.sidebar:
    st.header("👤 乘客登录")
    username = st.text_input("用户名")
    wallet = st.text_input("Pi 钱包地址")
    if st.button("登录", type="primary", use_container_width=True):
        if username and wallet:
            st.session_state.username = username
            st.session_state.wallet = wallet
            st.success(f"欢迎，{username}！")
        else:
            st.error("请填写用户名和钱包地址")

    st.markdown("---")
    st.caption(f"网络: Testnet | App: {APP_ID}")

# 主内容区
if 'username' not in st.session_state:
    st.info("👈 请先在左侧登录")
else:
    # 叫车表单
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 我要打车")

        pickup = st.text_input("上车地点", placeholder="例如：江南水岸七组团")
        destination = st.text_input("目的地", placeholder="例如：重庆北站")

        car_type = st.selectbox(
            "选择车型",
            ["economy", "comfort", "premium"],
            format_func=lambda x: {"economy": "经济型", "comfort": "舒适型", "premium": "豪华型"}[x]
        )

        distance = st.slider("预估里程（公里）", 1, 50, 10)
        price = calculate_price(distance, car_type)

        st.info(f"💰 预估价格：**{price} Pi**")

        if st.button("🚗 立即叫车", type="primary", use_container_width=True):
            if pickup and destination:
                order = {
                    "id": f"ORD{int(time.time())}",
                    "passenger": st.session_state.username,
                    "wallet": st.session_state.wallet,
                    "pickup": pickup,
                    "destination": destination,
                    "car_type": car_type,
                    "price": price,
                    "status": "pending",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "driver": None
                }
                st.session_state.orders.append(order)
                st.session_state.current_order = order
                st.success(f"✅ 叫车成功！订单号：{order['id']}")
                st.rerun()
            else:
                st.error("⚠️ 请填写上车地点和目的地")

    with col2:
        st.subheader("📋 我的订单")

        my_orders = [o for o in st.session_state.orders if o["passenger"] == st.session_state.username]

        if my_orders:
            for order in reversed(my_orders[-5:]):
                status_map = {
                    "pending": "🟡 等待接单",
                    "accepted": "🟢 司机已接单",
                    "in_progress": "🔵 行程中",
                    "completed": "✅ 已完成",
                    "cancelled": "❌ 已取消"
                }
                with st.container(border=True):
                    st.write(f"**订单号：{order['id']}**")
                    st.write(f"📍 {order['pickup']} → 🏁 {order['destination']}")
                    st.write(f"💰 {order['price']} Pi | {status_map.get(order['status'], order['status'])}")
                    if order["driver"]:
                        st.write(f"🚕 司机：{order['driver']}")
        else:
            st.info("暂无订单")

st.markdown("---")
st.caption("RideGo 乘客端 v1.0 | Powered by Pi Network")

import streamlit as st

# 預設機型與功率
devices = {
    "CT-AQ5H": 2939,
    "CT-AQ10H": 3364,
    "CT-AQ25H": 7974,
    "CT-AQ100H": 26960,
    "CT-AQ125H": 46475,
    "靈巧型-6H": 2200,
    #可新增機型
}

# 預設電價方案
electricity_rates = {
    "2025夏季電價": {
        "【平日】尖峰期": 6.89,
        "【平日】半尖峰期": 4.26,
        "【平日】離峰期": 1.9,
        "【週六】半尖峰期": 2.18,
        "【週六】離峰期": 1.9,
        "【週日】離峰期": 1.9,
    },
    "非夏季電價": {
        "【平日】尖峰期": 3.50,
        "【平日】半尖峰期": 2.85,
        "【平日】離峰期": 2.20,
        "【週六】半尖峰期": 2.60,
        "【週六】離峰期": 2.10,
        "【週日】離峰期": 1.95,
    }
}

labels = [
    "【平日】尖峰期", "【平日】半尖峰期", "【平日】離峰期",
    "【週六】半尖峰期", "【週六】離峰期", "【週日】離峰期"
]

# 設定頁面
st.set_page_config(page_title="電費計算器", layout="wide")

st.title("📱 電費計算器（手機可用）")

# 選擇機型
device = st.selectbox("選擇機型", list(devices.keys()))
watt = devices[device]
kwh = watt / 1000
st.write(f"💡 消耗電力：{watt} W（= {kwh:.3f} 度 / 每小時）")

# 選擇電價方案
scheme = st.selectbox("選擇電價方案", list(electricity_rates.keys()), index=0)
rates = electricity_rates[scheme]

st.markdown("---")

total_kwh = 0
total_cost = 0

# 建立每個時段輸入欄
for label in labels:
    st.subheader(label)
    cols = st.columns([1, 1, 2])

    rate = rates[label]
    cols[0].markdown(f"💰 每度電：{rate:.2f} 元")
    hours = cols[1].number_input(f"{label} 使用時數", min_value=0.0, step=0.5, key=label)

    # 計算
    per_hour_cost = kwh * rate
    total_kwh_segment = kwh * hours
    total_cost_segment = per_hour_cost * hours

    total_kwh += total_kwh_segment
    total_cost += total_cost_segment

    cols[2].markdown(
        f"""
        - 每小時電費：{per_hour_cost:.2f} 元  
        - 小計度數：{total_kwh_segment:.2f} 度  
        - 小計電費：{total_cost_segment:.2f} 元
        """
    )

st.markdown("---")
st.success(f"🔢 **總度數：{total_kwh:.2f} 度**")
st.success(f"💵 **總電費：{total_cost:.2f} 元**")

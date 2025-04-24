import streamlit as st
import math

# ✅ 必須放在最上方
st.set_page_config(page_title="圓華ESG計算工具", layout="wide")

# Logo + 標題區塊
def show_logo_header(image_file):
    st.image(image_file, width=300)
    st.markdown(
        """
        <h1 style='text-align: center;'>🌱💧 圓華油品股份有限公司ESG設備電費計算系統 💧🌱</h1>
        <p style='text-align: center; font-size: 14px; color: gray;'>製作人員：Sheng</p>
        """,
        unsafe_allow_html=True
    )

# 顯示 Logo
show_logo_header("Company's_Logo_1.png")

# 建立選單選項
page = st.sidebar.radio("選擇頁面", ["電費計算器", "消泡劑成本試算"])

if page == "電費計算器":
    # 預設機型與功率
    devices = {
        "CT-AQ5H": 2939,
        "CT-AQ10H": 3364,
        "CT-AQ25H": 7974,
        "CT-AQ100H": 26960,
        "CT-AQ125H": 46475,
        "靈巧型-6H": 2200,
    }

    electricity_rates = {
        "2025夏季電價": {
            "【平日】尖峰期": 6.89,
            "【平日】半尖峰期": 4.26,
            "【平日】離峰期": 1.9,
            "【週六】半尖峰期": 2.18,
            "【週六】離峰期": 1.9,
            "【週日】離峰期": 1.9,
        },
        "夏季電價": {
            "【平日】尖峰期": 3.89,
            "【平日】半尖峰期": 3.13,
            "【平日】離峰期": 2.50,
            "【週六】半尖峰期": 2.80,
            "【週六】離峰期": 2.30,
            "【週日】離峰期": 2.10
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

    device = st.selectbox("選擇機型", list(devices.keys()))
    watt = devices[device]
    kwh = watt / 1000
    st.write(f"💡 消耗電力：{watt} W（= {kwh:.3f} 度 / 每小時）")

    custom_rate = st.checkbox("✏️ 使用自訂電價")

    if custom_rate:
        st.markdown("🧾 **請輸入每個時段的電價（元/度）**")
        rates = {}
        for label in labels:
            rate_input = st.number_input(f"{label} 每度電價", min_value=0.0, step=0.1, key=f"{label}_custom_rate")
            rates[label] = rate_input
    else:
        scheme = st.selectbox("選擇電價方案", list(electricity_rates.keys()), index=0)
        rates = electricity_rates[scheme]

    st.markdown("---")

    total_kwh = 0
    total_cost = 0

    for label in labels:
        st.subheader(label)
        cols = st.columns([1, 1, 2])
        rate = rates[label]
        cols[0].markdown(f"💰 每度電：{rate:.2f} 元")
        hours = cols[1].number_input(f"{label} 使用時數", min_value=0.0, step=0.5, key=label)

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

elif page == "消泡劑成本試算":
    st.header("🧪 消泡劑成本試算")

    ratio_raw = st.text_input("輸入稀釋比例（格式為 原液:水，例如 1:19）", value="1:19")
    price_per_barrel = st.number_input("每桶原液價格（元）", value=15000)
    volume_per_barrel = st.number_input("每桶原液容量（L）", value=15.0)
    dilute_usage = st.number_input("每多少 L 稀釋液可處理廢液量（L）", value=3.0)
    waste_treated_per_dilute = st.number_input("對應可處理廢液量（L）", value=810.0)
    waste_input = st.number_input("欲處理的廢液量（L）", min_value=0.0, value=3000.0)

    try:
        ratio_parts = list(map(float, ratio_raw.split(":")))
        if len(ratio_parts) == 2 and ratio_parts[0] > 0:
            dilute_factor = sum(ratio_parts)
            dilute_per_barrel = volume_per_barrel * dilute_factor
            waste_per_barrel = dilute_per_barrel * (waste_treated_per_dilute / dilute_usage)
            cost_per_liter = price_per_barrel / waste_per_barrel
            total_cost = waste_input * cost_per_liter

            st.markdown("""
            ### 🧾 成本計算結果
            - 每桶可稀釋量：約 {:.2f} L 稀釋液
            - 每桶可處理：約 {:.0f} L 廢液
            - 每 1,000L 廢液成本：約 {:.2f} 元
            - ✅ 預估總成本：約 {:.2f} 元
            """.format(
                dilute_per_barrel,
                waste_per_barrel,
                cost_per_liter * 1000,
                total_cost
            ))
            st.markdown(
    """
    <p style='text-align: center; color: gray; font-size: 14px;'>
    📌 備註：以上試算結果僅供參考，實際成本將依據機台與處理液性質、消泡劑品牌及價格有所不同。
    </p>
    """,
    unsafe_allow_html=True
)

        else:
            st.warning("請輸入正確的稀釋比例格式，例如 1:19")
    except:
        st.warning("請確認稀釋比例格式正確，例如 1:19")
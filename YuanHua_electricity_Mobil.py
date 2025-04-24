import streamlit as st

# ✅ 必須為第一個指令
st.set_page_config(page_title="電費計算器", layout="wide")

# Logo 標題

def show_logo_header(image_file):
    st.image(image_file, width=300)
    st.markdown(
        """
        <h1 style='text-align: center;'>🌱💧 圓華油品股份有限公司ESG設備計算系統 💧🌱</h1>
        <p style='text-align: center; font-size: 14px; color: gray;'>製作人員：Sheng</p>
        """,
        unsafe_allow_html=True
    )

# 呼叫設定
show_logo_header("Company's_Logo_1.png")

# 分頁選單
page = st.sidebar.selectbox("請選擇功能頁面", ["電費計算", "消泡劑成本試算", "原液削減率"])

if page == "電費計算":
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

    ratio_part1 = st.number_input("原液比例 (例如 1:19 中的 1)", min_value=0.0, value=1.0)
    ratio_part2 = st.number_input("水比例 (例如 1:19 中的 19)", min_value=0.0, value=19.0)
    total_dilution = ratio_part1 + ratio_part2

    bucket_volume = st.number_input("每桶原液容量 (L)", min_value=0.0, value=15.0)
    bucket_price = st.number_input("每桶原液價格 (元)", min_value=0.0, value=15000.0)

    treat_per_x_liters = st.number_input("稀釋液使用量 (L)", min_value=0.1, value=3.0)
    waste_per_treatment = st.number_input("每份稀釋液可處理原液量 (L)", min_value=0.0, value=810.0)

    diluted_total = bucket_volume * total_dilution
    treatable_waste = diluted_total / treat_per_x_liters * waste_per_treatment

    st.markdown(f"💧 每桶可稀釋：**{diluted_total:.2f}L** 稀釋液")
    st.markdown(f"♻️ 每桶可處理：**{treatable_waste:.2f}L** 原液")

    st.markdown(f"💰 成本為：**{bucket_price:.2f} 元**")

    input_waste = st.number_input("想處理的原液量 (L)", min_value=0.0, value=3000.0)
    if treatable_waste > 0:
        cost_for_input = (bucket_price / treatable_waste) * input_waste
        st.markdown(f"📦 處理 {input_waste:.0f}L 原液的成本為：**{cost_for_input:.2f} 元**")

    st.info("🔍 註：因機台及處理液之屬性、消泡劑價格不同而有所差異")

elif page == "原液削減率":
    st.header("🧮 原液削減率計算")

    supply = st.number_input("總供應原液量 (L)", min_value=0.0)
    concentrate = st.number_input("濃縮液量 (L)", min_value=0.0)

    if concentrate > 0:
        multiple = supply / concentrate
        reduction_rate = 100 - (100 / multiple)

        st.markdown(f"🔁 **倍率：{multiple:.2f} 倍**")
        st.markdown(f"📉 **削減率：{reduction_rate:.2f}%**")
    else:
        st.warning("請輸入有效的濃縮液量 (不可為 0)")
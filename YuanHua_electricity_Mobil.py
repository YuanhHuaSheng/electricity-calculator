import streamlit as st

# ✅ 這一定要是第一個 Streamlit 指令
st.set_page_config(page_title="圓華ESG工具", layout="wide")

# 共用 LOGO 標題區塊
def show_logo_header():
    st.image("Company's_Logo_1.png", width=300)
    st.markdown("""
    <h1 style='text-align: center;'>
    🌱💧 圓華油品股份有限公司ESG設備電費計算系統 💧🌱
    </h1>
    <p style='text-align: center; font-size: 14px; color: gray;'>製作人員：Sheng</p>
    """, unsafe_allow_html=True)

# 分頁選單
page = st.sidebar.radio("請選擇功能頁面：", [
    "電費計算器", 
    "消泡劑成本試算",
    "原液削減率",
    "原液處理能力"
])

show_logo_header()

if page == "電費計算器":
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
    st.write(f"⚡️ 消耗電力：{watt} W（= {kwh:.3f} 度 / 每小時）")

    custom_rate = st.checkbox("✏️ 使用自訂電價")
    if custom_rate:
        st.markdown("📃 **請輸入每個時段的電價（元/度）**")
        rates = {label: st.number_input(f"{label} 每度電價", min_value=0.0, step=0.1, key=f"{label}_custom") for label in labels}
    else:
        scheme = st.selectbox("選擇電價方案", list(electricity_rates.keys()), index=0)
        rates = electricity_rates[scheme]

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

        cols[2].markdown(f"""
        - 每小時電費：{per_hour_cost:.2f} 元  
        - 小計度數：{total_kwh_segment:.2f} 度  
        - 小計電費：{total_cost_segment:.2f} 元
        """)

    st.markdown("---")
    st.success(f"🔢 **總度數：{total_kwh:.2f} 度**")
    st.success(f"💵 **總電費：{total_cost:.2f} 元**")

elif page == "消泡劑成本試算":
    st.header("消泡劑成本試算")

    ratio = st.number_input("稀釋比例 (原液 : 水)", min_value=1.0, value=1.0)
    total_parts = ratio + 19
    unit_name = f"1:{int(19)}" if ratio == 1.0 else f"1:{int(total_parts - 1)}"

    price = st.number_input("每桶原液售價 (元)", min_value=0.0, value=15000.0)
    volume = st.number_input("每桶原液容量 (L)", min_value=0.0, value=15.0)
    diluted_amount_per_bucket = volume * total_parts

    st.write(f"每桶原液可稀釋為 {diluted_amount_per_bucket:.2f} L 稀釋液")

    diluted_use = st.number_input("每 __L__ 稀釋液可處理原液量 (L)", value=3.0)
    waste_per_unit = st.number_input("該稀釋液處理原液量 (L)", value=810.0)

    waste_per_liter_diluted = waste_per_unit / diluted_use if diluted_use else 0
    waste_capacity = diluted_amount_per_bucket * waste_per_liter_diluted
    cost_per_1000L = price / (waste_capacity / 1000) if waste_capacity else 0

    st.success(f"♻️ 一桶原液可處理約 {waste_capacity:,.0f} L 原液")
    st.success(f"💰 處理 1,000L 原液成本：約 {cost_per_1000L:.2f} 元")
    st.caption("\n因機台及處理液之屬性、消泡劑價格不同而有所差異")

elif page == "原液削減率":
    st.header("原液削減率試算")
    supply = st.number_input("總供應原液量 (L)", min_value=0.0)
    concentrate = st.number_input("濃縮液量 (L)", min_value=0.0)

    if concentrate > 0:
        multiple = supply / concentrate
        reduction_rate = 100 - (100 / multiple)
        st.success(f"削減倍率：{multiple:.2f} 倍")
        st.success(f"原液削減率：約 {reduction_rate:.2f} %")
    else:
        st.warning("請輸入有效的濃縮液量")

elif page == "原液處理能力":
    st.header("原液處理能力計算")
    total_volume = st.number_input("單次總供應原液量 (L)", min_value=0.0)
    process_time = st.number_input("單次濃縮時間 (分鐘)", min_value=1.0)

    capacity = total_volume / process_time * 60
    st.success(f"處理能力：約 {capacity:.2f} 公升 / 小時")

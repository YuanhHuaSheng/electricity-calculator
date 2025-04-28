import streamlit as st

# 設定頁面
st.set_page_config(page_title="電費計算器", layout="wide")

# 顯示 Logo + 頁首
def show_logo_header(image_file):
    st.image(image_file, width=300)
    st.markdown(
    """
    <h1 style='text-align: center;'>🌱💧 圓華油品股份有限公司ESG設備計算系統 💧🌱</h1>
    <p style='text-align: center; font-size: 14px; color: gray;'>製作人員：Sheng</p>
    """,
    unsafe_allow_html=True
    )

# 電費計算頁面
def electricity_page():
    st.header("🔌 電費計算器")
    
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
    st.write(f"⚡ 消耗電力：{watt} W（= {kwh:.3f} 度 / 每小時）")

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

# 消泡劑成本試算
def defoamer_cost_page():
    st.header("🧪 消泡劑成本試算")

    st.markdown("### 基本設定")
    ratio_input = st.text_input("稀釋比例（格式：原液:水）", "1:19")
    bucket_volume = st.number_input("每桶消泡劑容量 (L)", value=15.0, step=1.0)
    bucket_price = st.number_input("每桶售價 (元)", value=15000.0, step=100.0)
    waste_per_x_liters = st.number_input("每 X 公升稀釋液可處理的廢液量 (L)", value=810.0, step=10.0)
    x_liters = st.number_input("X（稀釋液使用量，單位：L）", value=3.0, step=0.5)
    target_waste = st.number_input("預計處理的廢液量 (L)", value=3000.0, step=100.0)

    try:
        parts = ratio_input.split(":")
        concentrate_part = float(parts[0])
        water_part = float(parts[1])
        total_ratio = concentrate_part + water_part

        diluted_per_concentrate = total_ratio
        total_diluted = bucket_volume * diluted_per_concentrate
        concentrate_used = bucket_volume
        water_used = bucket_volume * (water_part / concentrate_part)

        waste_per_liter_diluted = waste_per_x_liters / x_liters
        total_waste_handled = total_diluted * waste_per_liter_diluted
        cost_per_1000L = bucket_price / (total_waste_handled / 1000)
        cost_for_target = (target_waste / total_waste_handled) * bucket_price

        st.markdown("### 試算結果")
        st.info(f"📦 每桶可稀釋出稀釋液量：約 **{total_diluted:.2f} L**")
        st.info(f"🧫 使用原液量：約 **{concentrate_used:.2f} L**，使用水量：約 **{water_used:.2f} L**")
        st.info(f"🧪 每 1 L 稀釋液可處理廢液量：約 **{waste_per_liter_diluted:.2f} L**")
        st.info(f"🧫 每桶原液可處理廢液量：約 **{total_waste_handled:,.0f} L**")
        st.success(f"💰 每 1,000L 廢液處理成本：約 **{cost_per_1000L:.2f} 元**")
        st.success(f"🧾 預估處理 {target_waste:.0f}L 廢液的成本：約 **{cost_for_target:.2f} 元**")

    except Exception as e:
        st.error("⚠️ 請確認輸入格式是否正確（例如：1:19）")
        st.error(f"詳細錯誤：{e}")

    st.caption("🔍 備註：因機台及處理液之屬性、消泡劑價格不同而有所差異")

# 原液削減率
def reduction_rate_page():
    st.header("📉 原液削減率計算")
    total_supply = st.number_input("總供應原液量 (L)", min_value=0.0, step=1.0)
    concentrate_volume = st.number_input("濃縮液量 (L)", min_value=0.0, step=1.0)

    if concentrate_volume == 0:
        st.warning("請輸入有效的濃縮液量")
    else:
        multiple = total_supply / concentrate_volume
        reduction_rate = 100 - (100 / multiple)
        st.info(f"🔁 濃縮倍率：{multiple:.2f} 倍")
        st.success(f"📉 削減率：約 {reduction_rate:.2f}%")

# 原液處理能力
def capacity_page():
    st.header("⚙️ 原液處理能力")
    total_supply = st.number_input("總供應原液量 (L)", min_value=0.0, step=1.0)
    time_per_batch = st.number_input("單次濃縮時間 (分鐘)", min_value=0.0, step=1.0)

    if time_per_batch == 0:
        st.warning("請輸入有效的濃縮時間")
    else:
        capacity = (total_supply / time_per_batch) * 60
        st.success(f"📦 處理能力：約 {capacity:.2f} L/hr")

# 私人專區登入
def private_login_page():
    st.header("🔒 私人專區登入")
    
    accounts = {
        "admin": "1234",
        "cost": "142205"
    }

    id_input = st.text_input("請輸入 ID")
    pw_input = st.text_input("請輸入密碼", type="password")

    if st.button("登入"):
        if id_input in accounts and pw_input == accounts[id_input]:
            st.success("✅ 登入成功！歡迎進入私人專區。")
            st.markdown("### 🎉 私人專屬內容")
            st.markdown("- 機密資料一")
            st.markdown("- 機密資料二")
            st.markdown("- 機密資料三")
        else:
            st.error("❌ 登入失敗，請檢查 ID 或密碼是否正確。")

# 主程式區
show_logo_header("Company's_Logo_1.png")

main_menu = st.sidebar.selectbox("請選擇主題", [
    "🌱💧 ESG設備計算專區 💧🌱",
    "🔒 私人專區"
])

if main_menu == "🌱💧 ESG設備計算專區 💧🌱":
    esg_page = st.sidebar.selectbox("ESG設備選單", [
        "🔌 電費計算器",
        "🧪 消泡劑成本試算",
        "📉 原液削減率",
        "⚙️ 原液處理能力"
    ])

    if esg_page == "🔌 電費計算器":
        electricity_page()
    elif esg_page == "🧪 消泡劑成本試算":
        defoamer_cost_page()
    elif esg_page == "📉 原液削減率":
        reduction_rate_page()
    elif esg_page == "⚙️ 原液處理能力":
        capacity_page()

elif main_menu == "🔒 私人專區":
    private_login_page()

import streamlit as st
import pandas as pd
import datetime

# ---------- 設定頁面 ----------
st.set_page_config(page_title="電費計算器", layout="wide")

# ---------- Logo + 頁首 ----------
def show_logo_header(image_file):
    st.image(image_file, width=300)
    st.markdown(
        """
        <h1 style='text-align: center;'>🌱💧 圓華油品股份有限公司ESG設備計算系統 💧🌱</h1>
        <p style='text-align: center; font-size: 14px; color: gray;'>製作人員：Sheng</p>
        """,
        unsafe_allow_html=True
    )

# ---------- 電費計算器 ----------
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

# ---------- 消泡劑成本試算 ----------
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
        total_diluted = bucket_volume * total_ratio
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

# ---------- 原液削減率計算 ----------
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

# ---------- 原液處理能力 ----------
def capacity_page():
    st.header("⚙️ 原液處理能力")
    total_supply = st.number_input("總供應原液量 (L)", min_value=0.0, step=1.0)
    time_per_batch = st.number_input("單次濃縮時間 (分鐘)", min_value=0.0, step=1.0)
    if time_per_batch == 0:
        st.warning("請輸入有效的濃縮時間")
    else:
        capacity = (total_supply / time_per_batch) * 60
        st.success(f"📦 處理能力：約 {capacity:.2f} L/hr")

# ---------- 私人專區登入 ----------

def private_login_page():
    st.header("🔒 私人專區登入")
    accounts = {
        "admin": "1234",
        "cost": "142205",
        "login": "1111"
    }

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = ""

    def login_callback():
        id_input = st.session_state["id_input"]
        pw_input = st.session_state["pw_input"]
        if id_input in accounts and pw_input == accounts[id_input]:
            st.session_state["logged_in"] = True
            st.session_state["user"] = id_input
        else:
            st.session_state["login_error"] = True

    def logout_callback():
        st.session_state["logged_in"] = False
        st.session_state["user"] = ""
        # 清除錯誤訊息
        st.session_state["login_error"] = False

    if "login_error" not in st.session_state:
        st.session_state["login_error"] = False

    if st.session_state["logged_in"]:
        st.success(f"✅ 已登入，用戶：{st.session_state['user']}")
        st.button("登出", on_click=logout_callback)
    else:
        st.text_input("請輸入 ID", key="id_input")
        st.text_input("請輸入密碼", type="password", key="pw_input")
        st.button("登入", on_click=login_callback)
        if st.session_state["login_error"]:
            st.error("❌ ID 或密碼錯誤，請重新輸入。")

# ---------- 庫存管理功能 ----------
# 權限分級 - 僅 admin 可管理分類與使用者，cost 可調整庫存，login 只可看
def inventory_page():
    if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
        st.warning("請先登入私人專區以使用庫存管理功能。")
        return

    user = st.session_state.get("user", "")
    st.header(f"📦 庫存管理系統 (用戶：{user})")

    # 初始化資料儲存
    if "inventory_data" not in st.session_state:
        st.session_state["inventory_data"] = pd.DataFrame(columns=["分類", "品名", "數量"])
    if "categories" not in st.session_state:
        st.session_state["categories"] = ["消泡劑", "機器零件", "包裝材料","CT-AQ25H","CT-AQ100H","CT-AQ125H"]
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # 權限判斷
    is_admin = (user == "admin")
    can_edit = (user in ["admin", "cost"])
    can_view = True

    # 分頁：分類管理、庫存管理、歷史紀錄
    tabs = st.tabs(["庫存管理", "分類管理", "歷史紀錄"])

    # --- 庫存管理 ---
    with tabs[0]:
        st.subheader("🔹 庫存管理")
        df = st.session_state["inventory_data"]
        st.dataframe(df, use_container_width=True)

        if can_edit:
            st.markdown("### 新增庫存項目")
            col1, col2, col3 = st.columns(3)
            with col1:
                new_category = st.selectbox("選擇分類", st.session_state["categories"], key="new_item_category")
            with col2:
                new_item = st.text_input("品名", key="new_item_name")
            with col3:
                new_qty = st.number_input("數量", min_value=0, step=1, key="new_item_qty")

            if st.button("新增庫存項目"):
                if new_item.strip() == "":
                    st.warning("品名不可為空")
                else:
                    # 避免重複品項
                    if ((df["品名"] == new_item) & (df["分類"] == new_category)).any():
                        st.warning("此分類下已有相同品名，請勿重複新增。")
                    else:
                        new_row = {"分類": new_category, "品名": new_item, "數量": new_qty}
                        st.session_state["inventory_data"] = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                        st.success("新增成功！")

            st.markdown("---")
            st.markdown("### 調整庫存數量")
            df = st.session_state["inventory_data"]
            if df.empty:
                st.info("目前庫存為空。")
            else:
                selected_item = st.selectbox("選擇品項", df["品名"] + " (" + df["分類"] + ")")
                selected_index = df.index[df["品名"] + " (" + df["分類"] + ")" == selected_item][0]
                current_qty = df.at[selected_index, "數量"]
                adjust_qty = st.number_input("調整數量 (+為增加，-為減少)", value=0, step=1)
                if st.button("確認調整"):
                    new_qty = current_qty + adjust_qty
                    if new_qty < 0:
                        st.error("庫存數量不可為負數！")
                    else:
                        st.session_state["inventory_data"].at[selected_index, "數量"] = new_qty
                        st.session_state["history"].append({
                            "時間": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "使用者": user,
                            "操作": f"{'增加' if adjust_qty>0 else '減少'}庫存",
                            "品名": df.at[selected_index, "品名"],
                            "分類": df.at[selected_index, "分類"],
                            "調整量": adjust_qty,
                            "調整後數量": new_qty
                        })
                        st.success(f"庫存已更新為 {new_qty}。")

        else:
            st.info("您沒有調整庫存的權限。")

    # --- 分類管理 ---
    with tabs[1]:
        if is_admin:
            st.subheader("🔸 分類管理 (限 Admin)")
            categories = st.session_state["categories"]
            st.write("現有分類：", categories)
            new_cat = st.text_input("新增分類名稱")
            if st.button("新增分類"):
                if new_cat.strip() == "":
                    st.warning("分類名稱不可為空")
                elif new_cat in categories:
                    st.warning("此分類已存在")
                else:
                    categories.append(new_cat)
                    st.session_state["categories"] = categories
                    st.success("新增分類成功！")

            st.markdown("---")
            del_cat = st.selectbox("刪除分類", options=categories)
            if st.button("刪除分類"):
                # 刪除分類前，確認庫存是否有該分類的品項
                df = st.session_state["inventory_data"]
                if (df["分類"] == del_cat).any():
                    st.error("此分類有庫存品項，不可刪除。請先移除相關品項。")
                else:
                    categories.remove(del_cat)
                    st.session_state["categories"] = categories
                    st.success("分類已刪除")
        else:
            st.subheader("🔸 分類管理")
            st.info("您沒有管理分類的權限")

    # --- 歷史紀錄 ---
    with tabs[2]:
        st.subheader("📜 操作歷史紀錄")
        history = st.session_state["history"]
        if len(history) == 0:
            st.info("目前尚無歷史紀錄")
        else:
            df_history = pd.DataFrame(history)
            st.dataframe(df_history.sort_values(by="時間", ascending=False))

# ---------- 主程式入口 ----------
def main():
    show_logo_header(Company's_Logo_1.png")  # 若有 logo.png，否則可改成 st.title
    menu = ["電費計算器", "消泡劑成本試算", "原液削減率", "原液處理能力", "私人專區", "庫存管理專區"]
    choice = st.sidebar.selectbox("功能選單", menu)

    if choice == "電費計算器":
        electricity_page()
    elif choice == "消泡劑成本試算":
        defoamer_cost_page()
    elif choice == "原液削減率":
        reduction_rate_page()
    elif choice == "原液處理能力":
        capacity_page()
    elif choice == "私人專區":
        private_login_page()
    elif choice == "庫存管理專區":
        inventory_page()

if __name__ == "__main__":
    main()

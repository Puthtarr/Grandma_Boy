import streamlit as st
from submit_to_gsheet import submit_orders_to_sheet

# ---------- DATA ----------
categories = {"ต้ม": 50, "ผัด": 45, "เส้น": 40, "ข้าวคลุก": 55}
meats = {"หมู": 0, "ไก่": 5, "เนื้อ": 10, "ทะเล": 15}
toppings = {"ไข่ดาว": 10, "ไข่เจียว": 10, "ไข่ต้ม": 8}
sizes = {"ธรรมดา": 0, "พิเศษ": 10}

# ---------- STATE ----------
if "step" not in st.session_state:
    st.session_state.step = "category"
if "orders" not in st.session_state:
    st.session_state.orders = []

# ---------- STEP: CATEGORY ----------
if st.session_state.step == "category":
    st.title("🍽️ เลือกหมวดอาหาร")

    image_map = {
        "ต้ม": "images/tom.jpg",
        "ผัด": "images/pad.jpg",
        "เส้น": "images/noodle.jpg",
        "ข้าวคลุก": "images/mixrice.jpg"
    }

    cols = st.columns(2)
    for i, (cat, price) in enumerate(categories.items()):
        with cols[i % 2]:
            st.image(image_map[cat], use_container_width=True)
            if st.button(f"{cat} ({price} บาท)", key=f"cat_{cat}"):
                st.session_state.temp = {
                    "หมวดหมู่": cat,
                    "base_price": price
                }
                st.session_state.step = "meat"
                st.rerun()

# ---------- STEP: MEAT ----------
elif st.session_state.step == "meat":
    st.title(f"🍳 เลือกเนื้อสัตว์สำหรับ {st.session_state.temp['หมวดหมู่']}")

    for meat, add_price in meats.items():
        if st.button(f"{meat} (+{add_price} บาท)"):
            st.session_state.temp["เนื้อ"] = meat
            st.session_state.temp["meat_price"] = add_price
            st.session_state.step = "toppings"
            st.rerun()

# ---------- STEP: TOPPINGS ----------
elif st.session_state.step == "toppings":
    st.title("🥚 เลือกท็อปปิ้ง")

    for topping, topping_price in toppings.items():
        if st.button(f'{topping} (+{topping_price} บาท)'):
            st.session_state.temp["ทอปปิ้ง"] = topping
            st.session_state.temp["topping_price"] = topping_price
            st.session_state.step = "size"
            st.rerun()

# ---------- STEP: SIZE ----------
elif st.session_state.step == "size":
    st.markdown("<h2 style='font-size: 32px;'>🍚 เลือกขนาดอาหาร</h2>", unsafe_allow_html=True)

    # CSS สำหรับปรับปุ่มให้ใหญ่ขึ้น (เพิ่มด้านบนถ้ายังไม่ได้ใส่)
    st.markdown("""
        <style>
        div.stButton > button {
            font-size: 24px;
            padding: 20px 36px;
            border-radius: 12px;
            width: 100%;
            background-color: #f0f0f0;
            color: black;
            border: 2px solid #888;
        }
        div.stButton > button:hover {
            background-color: #e0e0e0;
            border-color: #555;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ ธรรมดา", key="btn_normal"):
            st.session_state.temp["ขนาด"] = "ธรรมดา"
            st.session_state.temp["size_price"] = sizes["ธรรมดา"]

            total = (
                    st.session_state.temp["base_price"]
                    + st.session_state.temp["meat_price"]
                    + st.session_state.temp["topping_price"]
                    + st.session_state.temp["size_price"]
            )
            st.session_state.temp["ราคา"] = total

            st.session_state.orders.append(st.session_state.temp)
            del st.session_state["temp"]
            st.session_state.step = "category"
            st.rerun()

    with col2:
        if st.button("✨ พิเศษ (+10 บาท)", key="btn_special"):
            st.session_state.temp["ขนาด"] = "พิเศษ"
            st.session_state.temp["size_price"] = sizes["พิเศษ"]

            total = (
                    st.session_state.temp["base_price"]
                    + st.session_state.temp["meat_price"]
                    + st.session_state.temp["topping_price"]
                    + st.session_state.temp["size_price"]
            )
            st.session_state.temp["ราคา"] = total

            st.session_state.orders.append(st.session_state.temp)
            del st.session_state["temp"]
            st.session_state.step = "category"
            st.rerun()

# ---------- STEP: SUMMARY ----------
st.sidebar.title("🧾 ออเดอร์ทั้งหมด")
total_all = 0
for i, order in enumerate(st.session_state.orders):
    with st.sidebar.expander(f"จาน {i+1} : {order['หมวดหมู่']} + {order['เนื้อ']}"):
        st.write(f"ขนาด: {order['ขนาด']}")
        st.write(f"ท็อปปิ้ง: {order.get('ทอปปิ้ง', '-')}")
        st.write(f"ราคารวมจานนี้: {order['ราคา']} บาท")
        total_all += order["ราคา"]

st.sidebar.markdown(f"### 💵 ยอดรวมทั้งหมด: {total_all} บาท")

# ✅ ปุ่ม Submit ออเดอร์ทั้งหมด
if len(st.session_state.orders) > 0:
    if st.sidebar.button("✅ ส่งออเดอร์ทั้งหมด"):
        submit_orders_to_sheet(st.session_state.orders)
        st.success("ส่งออเดอร์ไป Google Sheets เรียบร้อยแล้ว 🎉")
        st.write(st.session_state.orders)
        st.session_state.clear()
        st.rerun()
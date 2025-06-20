import streamlit as st

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
            st.image(image_map[cat], use_column_width=True)
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

    selected = st.multiselect("เลือกท็อปปิ้ง", list(toppings.keys()))
    if st.button("ถัดไป"):
        st.session_state.temp["ท็อปปิ้ง"] = selected
        st.session_state.temp["topping_price"] = sum([toppings[t] for t in selected])
        st.session_state.step = "size"
        st.rerun()

# ---------- STEP: SIZE ----------
elif st.session_state.step == "size":
    st.title("🍚 เลือกขนาด")

    size = st.radio("ขนาด:", list(sizes.keys()))
    if st.button("ยืนยันเมนูนี้"):
        st.session_state.temp["ขนาด"] = size
        st.session_state.temp["size_price"] = sizes[size]

        # ✅ คำนวณราคารวมของเมนูนี้
        total = (
            st.session_state.temp["base_price"]
            + st.session_state.temp["meat_price"]
            + st.session_state.temp["topping_price"]
            + st.session_state.temp["size_price"]
        )
        st.session_state.temp["ราคา"] = total

        # ✅ เพิ่มเข้า orders แล้ววนกลับหน้าแรก
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
        st.write(f"ท็อปปิ้ง: {', '.join(order['ท็อปปิ้ง']) if order['ท็อปปิ้ง'] else '-'}")
        st.write(f"ราคารวมจานนี้: {order['ราคา']} บาท")
        total_all += order["ราคา"]

st.sidebar.markdown(f"### 💵 ยอดรวมทั้งหมด: {total_all} บาท")

# ✅ ปุ่ม Submit ออเดอร์ทั้งหมด
if len(st.session_state.orders) > 0:
    if st.sidebar.button("✅ ส่งออเดอร์ทั้งหมด"):
        st.success("ส่งออเดอร์เรียบร้อยแล้ว 🎉")
        st.write(st.session_state.orders)
        st.session_state.clear()
        st.rerun()

import gspread
import json
import tempfile
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def submit_orders_to_sheet(orders):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # โหลดจาก secrets
    creds_dict = json.loads(st.secrets["google_sheets"]["creds_json"])

    # สร้างไฟล์ชั่วคราว
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp_file:
        json.dump(creds_dict, temp_file)
        temp_file.flush()
        creds = ServiceAccountCredentials.from_json_keyfile_name(temp_file.name, scope)
        client = gspread.authorize(creds)

    sheet = client.open("Grandma Boys").sheet1

    if sheet.row_count == 0 or not sheet.cell(1, 1).value:
        sheet.append_row(["date", "category", "meat", "topping", "size", "total price"])

    now = datetime.now().strftime("%Y-%m-%d")
    for order in orders:
        sheet.append_row([
            now,
            order["หมวดหมู่"],
            order["เนื้อ"],
            order.get("ทอปปิ้ง", "-"),
            order["ขนาด"],
            order["ราคา"]
        ])

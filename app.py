import streamlit as st
import math
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import io

# Page Config
st.set_page_config(page_title="Pro Clean Portal", layout="centered")

# Inventory Data
inventory = {
    "T180PC": {"desc": "T180 -- 42X34 PILLOW CASES", "price": 16.60, "weight": 2.0, "volume": 60},
    "T18036809": {"desc": "T180 -- 36X80X9 TWIN FITTED SHEET", "price": 65.40, "weight": 10.0, "volume": 300},
    "BT24488#": {"desc": "24X48 BATH TOWEL 8# 10/S", "price": 24.18, "weight": 8.0, "volume": 400},
    "BTRS8PLT": {"desc": "24X48 PLATINUM BATH TOWEL 8#", "price": 35.62, "weight": 8.5, "volume": 450},
    "GO275417": {"desc": "27X54 GREEN OCEAN BATH TOWEL 17#", "price": 68.43, "weight": 17.0, "volume": 600}
}

# PDF Generator Function
def create_pdf(po_num, date, items, total, boxes, weight, box_size):
    buf = io.BytesIO()
    p = canvas.Canvas(buf, pagesize=LETTER)
    p.setFont("Helvetica-Bold", 16); p.drawString(50, 750, "PURCHASE ORDER")
    p.setFont("Helvetica", 10); p.drawString(50, 730, f"PO #: {po_num}"); p.drawString(50, 715, f"Date: {date}")
    p.setFont("Helvetica-Bold", 10); p.drawString(350, 750, "BILL TO:")
    p.setFont("Helvetica", 10)
    p.drawString(350, 735, "Pro Clean")
    p.drawString(350, 720, "5155 Sugarloaf Parkway, Ste D")
    p.drawString(350, 705, "Lawrenceville, GA 30043")
    p.drawString(350, 690, "Email@procleanoofatl.com")
    p.line(50, 675, 550, 675)
    y = 650
    p.drawString(50, y, "SKU"); p.drawString(150, y, "Description"); p.drawString(350, y, "Qty"); p.drawString(450, y, "Total")
    p.line(50, y-5, 550, y-5)
    y -= 25
    for i in items:
        p.drawString(50, y, i['SKU']); p.drawString(150, y, i['Description'][:35]); p.drawString(350, y, str(i['Qty'])); p.drawString(450, y, f"${i['Total']:,.2f}")
        y -= 20
    p.line(50, y, 550, y); y -= 30
    p.drawString(50, y, f"Shipping: {boxes} Boxes ({box_size}) | Total Weight: {weight} lbs")
    p.setFont("Helvetica-Bold", 12); p.drawString(400, y, f"GRAND TOTAL: ${total:,.2f}")
    p.showPage(); p.save(); buf.seek(0)
    return buf

st.title("🛡️ Pro Clean Portal")
st.markdown("### 1. Build Order")
if 'order_list' not in st.session_state: st.session_state.order_list = []

c1, c2 = st.columns([3, 1])
with c1: selected_product = st.selectbox("Product Search", options=list(inventory.keys()), format_func=lambda x: f"{x} - {inventory[x]['desc']}")
with c2: qty = st.number_input("Qty", min_value=1, step=1)
if st.button("Add to Order"): st.session_state.order_list.append({"SKU": selected_product, "Qty": qty})

if st.session_state.order_list:
    df = pd.DataFrame(st.session_state.order_list)
    df['Description'] = df['SKU'].apply(lambda x: inventory[x]['desc'])
    df['Unit Price'] = df['SKU'].apply(lambda x: inventory[x]['price'])
    df['Total'] = df['Unit Price'] * df['Qty']
    st.table(df[['SKU', 'Description', 'Qty', 'Unit Price', 'Total']])
    
    st.markdown("### 2. Shipping Configuration")
    box_choice = st.radio("Box Size", ["16x16x16", "18x18x18"], horizontal=True)
    box_cap = (int(box_choice[:2])**3) * 0.85
    
    total_val = df['Total'].sum()
    total_vol = sum(inventory[i['SKU']]['volume'] * i['Qty'] for i in st.session_state.order_list)
    total_weight = sum(inventory[i['SKU']]['weight'] * i['Qty'] for i in st.session_state.order_list)
    num_boxes = math.ceil(total_vol / box_cap)

    if st.button("Generate PO"):
        po_id = f"LP-{datetime.now().strftime('%y%m%d-%H%M')}"
        date_str = datetime.now().strftime('%B %d, %Y')
        
        st.divider()
        st.success(f"PO {po_id} Generated Successfully.")
        
        # Download Section
        pdf_data = create_pdf(po_id, date_str, df.to_dict('records'), total_val, num_boxes, total_weight, box_choice)
        st.download_button(label="📥 Download PO as PDF", data=pdf_data, file_name=f"PO_{po_id}.pdf", mime="application/pdf")
        
        # Email Simulation
        st.divider()
        st.markdown("### 📧 Email Purchase Order")
        email_addr = st.text_input("Recipient Email", value="Email@procleanoofatl.com")
        if st.button("Send PO via Email"):
            st.info(f"Prototype Logic: Sending {po_id} to {email_addr}... Done!")

    if st.button("Clear Order"):
        st.session_state.order_list = []
        st.rerun()

import streamlit as st
import math
import pandas as pd

# Set Page Config for a professional look
st.set_page_config(page_title="Linen Pros B2B Portal", layout="wide")

# Product Data from your CSV
inventory = {
    "T180PC": {"desc": "T180 -- 42X34 PILLOW CASES", "uom": "DZ", "price": 16.60, "weight": 2.0, "volume": 60},
    "T18036809": {"desc": "T180 -- 36X80X9 TWIN FITTED SHEET", "uom": "DZ", "price": 65.40, "weight": 10.0, "volume": 300},
    "BT24488#": {"desc": "24X48 BATH TOWEL 8# 10/S", "uom": "DZ", "price": 24.18, "weight": 8.0, "volume": 400},
    "BTRS8PLT": {"desc": "24X48 PLATINUM BATH TOWEL 8#", "uom": "DZ", "price": 35.62, "weight": 8.5, "volume": 450},
    "GO275417": {"desc": "27X54 GREEN OCEAN BATH TOWEL 17#", "uom": "DZ", "price": 68.43, "weight": 17.0, "volume": 600}
}

st.title("📦 Linen Pros Order Automation")
st.markdown("### Move from Faxing to One-Click Shipping Calculations")

# Sidebar for Box Settings
st.sidebar.header("Warehouse Settings")
box_type = st.sidebar.selectbox("Standard Box Size", ["16x16x16", "18x18x18"])
box_dims = 16 if "16" in box_type else 18
box_capacity = (box_dims**3) * 0.90  # 90% utilization efficiency

# Main Order Form
st.subheader("1. Enter Order Details")
order_items = {}

col1, col2 = st.columns(2)
with col1:
    for sku, info in inventory.items():
        qty = st.number_input(f"{info['desc']} ({sku}) - ${info['price']}/{info['uom']}", min_value=0, step=1, key=sku)
        if qty > 0:
            order_items[sku] = qty

# Calculation Logic
if order_items:
    st.divider()
    st.subheader("2. Automation Output")
    
    total_vol = sum(inventory[sku]['volume'] * qty for sku, qty in order_items.items())
    total_weight = sum(inventory[sku]['weight'] * qty for sku, qty in order_items.items())
    total_price = sum(inventory[sku]['price'] * qty for sku, qty in order_items.items())
    
    num_boxes = math.ceil(total_vol / box_capacity)
    
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Total Order Value", f"${total_price:,.2f}")
    res_col2.metric("Calculated Boxes", f"{num_boxes} Units")
    res_col3.metric("Estimated Weight", f"{total_weight} lbs")

    # Generate the Digital PO
    st.info(f"Automation logic complete. Ready to generate PO for {num_boxes} boxes of {box_type}.")
    if st.button("Generate & Process Digital PO"):
        st.success("✅ Order Processed. Warehouse dimensions sent to carrier. No faxing required!")
else:
    st.write("Please enter a quantity above to see the boxing automation in action.")

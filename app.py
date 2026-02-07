import streamlit as st
import math
import pandas as pd
from datetime import datetime

# Set Page Config
st.set_page_config(page_title="Pro Clean Portal", layout="centered")

# [cite_start]Product Data from your list [cite: 1, 2, 4, 6]
inventory = {
    "T180PC": {"desc": "T180 -- 42X34 PILLOW CASES", "price": 16.60, "weight": 2.0, "volume": 60},
    "T18036809": {"desc": "T180 -- 36X80X9 TWIN FITTED SHEET", "price": 65.40, "weight": 10.0, "volume": 300},
    "BT24488#": {"desc": "24X48 BATH TOWEL 8# 10/S", "price": 24.18, "weight": 8.0, "volume": 400},
    "BTRS8PLT": {"desc": "24X48 PLATINUM BATH TOWEL 8#", "price": 35.62, "weight": 8.5, "volume": 450},
    "GO275417": {"desc": "27X54 GREEN OCEAN BATH TOWEL 17#", "price": 68.43, "weight": 17.0, "volume": 600}
}

st.title("🛡️ Pro Clean Portal")
st.subheader("Dimension & PO Generator")

# 1. Build Order Section
st.markdown("### 1. Build Order")
if 'order_list' not in st.session_state:
    st.session_state.order_list = []

col1, col2 = st.columns([3, 1])
with col1:
    selected_product = st.selectbox("Search or Select Product", options=list(inventory.keys()), 
                                    format_func=lambda x: f"{x} - {inventory[x]['desc']}")
with col2:
    quantity = st.number_input("Qty", min_value=1, step=1)

if st.button("Add to Order"):
    st.session_state.order_list.append({"SKU": selected_product, "Qty": quantity})

# Order Table
if st.session_state.order_list:
    df_order = pd.DataFrame(st.session_state.order_list)
    df_order['Description'] = df_order['SKU'].apply(lambda x: inventory[x]['desc'])
    df_order['Unit Price'] = df_order['SKU'].apply(lambda x: inventory[x]['price'])
    df_order['Total'] = df_order['Unit Price'] * df_order['Qty']
    
    # Reorder columns for display
    st.table(df_order[['SKU', 'Description', 'Qty', 'Unit Price', 'Total']])
    
    if st.button("Clear Order"):
        st.session_state.order_list = []
        st.rerun()

    st.divider()

    # 2. Shipping Configuration
    st.markdown("### 2. Shipping Configuration")
    box_choice = st.radio("Select Shipping Box Size", ["16x16x16", "18x18x18"], horizontal=True)
    box_dim = int(box_choice.split('x')[0])
    box_capacity = (box_dim**3) * 0.85 

    # Logic Calculations
    total_val = df_order['Total'].sum()
    total_vol = sum(inventory[item['SKU']]['volume'] * item['Qty'] for item in st.session_state.order_list)
    total_weight = sum(inventory[item['SKU']]['weight'] * item['Qty'] for item in st.session_state.order_list)
    num_boxes = math.ceil(total_vol / box_capacity)

    if st.button("Generate Professional PO"):
        st.divider()
        
        # --- PROFESSIONAL PO DOCUMENT ---
        with st.container(border=True):
            # Header
            h1, h2 = st.columns(2)
            with h1:
                st.markdown("### PURCHASE ORDER")
                st.markdown(f"**PO #:** LP-{datetime.now().strftime('%y%m%d-%H%M')}")
                st.markdown(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
            
            with h2:
                st.markdown("**BILL TO:**")
                st.markdown("""
                **Pro Clean** 5155 Sugarloaf Parkway, Ste D  
                Lawrenceville, GA 30043  
                Email@procleanoofatl.com
                """)
            
            st.write("---")
            
            # Itemized List
            st.dataframe(df_order[['SKU', 'Description', 'Qty', 'Unit Price', 'Total']], hide_index=True, use_container_width=True)
            
            st.write("---")
            
            # Totals and Shipping Data
            f1, f2 = st.columns(2)
            with f1:
                st.markdown("#### Shipping Details")
                st.write(f"**Total Boxes:** {num_boxes}")
                st.write(f"**Box Dimensions:** {box_choice}")
                st.write(f"**Est. Weight:** {total_weight} lbs")
            
            with f2:
                st.markdown("#### Summary")
                st.write(f"**Subtotal:** ${total_val:,.2f}")
                st.write(f"**Tax (0%):** $0.00")
                st.markdown(f"### **GRAND TOTAL: ${total_val:,.2f}**")
        
        st.caption("Internal Prototype: Dimensions calculated automatically via Pro Clean Portal Engine.")

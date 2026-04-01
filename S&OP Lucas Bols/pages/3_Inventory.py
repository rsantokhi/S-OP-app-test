"""PlanFlow Inventory Planning — Stock Management and Reorder Logic."""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import (
    load_item_info,
    load_orders_in,
    load_orders_out,
    get_monthly_demand,
)
from utils.forecast_engine import calculate_safety_stock
from utils.styling import COLORS

st.set_page_config(page_title="Inventory Planning | PlanFlow", layout="wide")

st.title("Inventory Planning")
st.markdown("Manage inventory levels, safety stock, and purchase order proposals.")

# Load data
items = load_item_info()
demand = get_monthly_demand()
orders_in = load_orders_in()
orders_out = load_orders_out()

# Calculate metrics for each item
items["avg_monthly_demand"] = items["item_code"].apply(
    lambda x: demand[demand["item_code"] == x]["quantity"].mean()
)

items["incoming_qty"] = items["item_code"].apply(
    lambda x: orders_in[orders_in["item_code"] == x]["quantity"].sum()
)

items["days_on_hand"] = items.apply(
    lambda x: (x["on_hand"] / (x["avg_monthly_demand"] / 30)) if x["avg_monthly_demand"] > 0 else 0,
    axis=1
)

# Calculate safety stock
items["safety_stock"] = items.apply(
    lambda x: calculate_safety_stock(
        pd.Series(demand[demand["item_code"] == x["item_code"]]["quantity"].values),
        x["lead_time_days"],
        service_level=0.98
    ),
    axis=1
)

items["reorder_point"] = items["safety_stock"] + items["avg_monthly_demand"] * (items["lead_time_days"] / 30)

# Identify items needing attention (below safety stock)
items["needs_attention"] = items["on_hand"] < items["safety_stock"]

# Tabs for different views
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "All Items",
    f"⚠️ Attention ({items['needs_attention'].sum()})",
    "Open Orders In",
    "Suppliers",
    "Order Proposals"
])

# TAB 1: All Items
with tab1:
    st.subheader("All Items")

    # Display all items in a table
    items_display = items[[
        "item_code",
        "description",
        "category",
        "on_hand",
        "safety_stock",
        "reorder_point",
        "lead_time_days",
        "avg_monthly_demand",
        "days_on_hand"
    ]].copy()

    items_display.columns = [
        "Item Code",
        "Description",
        "Category",
        "On Hand",
        "Safety Stock",
        "Reorder Point",
        "Lead Time (days)",
        "Avg Monthly Demand",
        "Days Supply"
    ]

    # Highlight rows where on-hand is below safety stock
    def highlight_row(row):
        if row["On Hand"] < row["Safety Stock"]:
            return ["background-color: rgba(232, 114, 12, 0.15)"] * len(row)
        return [""] * len(row)

    items_display["On Hand"] = items_display["On Hand"].astype(int)
    items_display["Safety Stock"] = items_display["Safety Stock"].astype(int)
    items_display["Reorder Point"] = items_display["Reorder Point"].astype(int)
    items_display["Avg Monthly Demand"] = items_display["Avg Monthly Demand"].astype(int)
    items_display["Days Supply"] = items_display["Days Supply"].astype(int)

    st.dataframe(
        items_display,
        use_container_width=True,
        height=500,
        column_config={
            col: st.column_config.NumberColumn(format="%d") for col in items_display.columns if col not in ["Item Code", "Description", "Category"]
        }
    )

# TAB 2: Attention Items
with tab2:
    st.subheader("Items Below Safety Stock")

    attention_items = items[items["needs_attention"]]

    if len(attention_items) > 0:
        attention_display = attention_items[[
            "item_code",
            "description",
            "on_hand",
            "safety_stock",
            "avg_monthly_demand",
            "lead_time_days",
            "supplier"
        ]].copy()

        attention_display.columns = [
            "Item Code",
            "Description",
            "On Hand",
            "Safety Stock",
            "Avg Monthly Demand",
            "Lead Time (days)",
            "Supplier"
        ]

        attention_display["On Hand"] = attention_display["On Hand"].astype(int)
        attention_display["Safety Stock"] = attention_display["Safety Stock"].astype(int)
        attention_display["Avg Monthly Demand"] = attention_display["Avg Monthly Demand"].astype(int)

        st.dataframe(
            attention_display,
            use_container_width=True,
            height=400,
        )

        st.warning(f"⚠️ {len(attention_items)} items require attention and may need expedited ordering!")

    else:
        st.success("✓ All items are above safety stock levels.")

# TAB 3: Open Orders In
with tab3:
    st.subheader("Purchase Orders to Receive")

    if len(orders_in) > 0:
        orders_in_display = orders_in[[
            "item_code",
            "location",
            "delivery_date",
            "quantity"
        ]].copy()

        orders_in_display.columns = ["Item Code", "Location", "Delivery Date", "Quantity"]
        orders_in_display["Quantity"] = orders_in_display["Quantity"].astype(int)

        st.dataframe(
            orders_in_display,
            use_container_width=True,
            height=300,
        )
    else:
        st.info("No open purchase orders.")

# TAB 4: Suppliers
with tab4:
    st.subheader("Supplier List")

    supplier_list = items[["supplier", "item_code", "on_hand", "avg_monthly_demand"]].copy()
    supplier_list = supplier_list.dropna(subset=["supplier"])
    supplier_summary = supplier_list.groupby("supplier").agg({
        "item_code": "count",
        "on_hand": "sum",
        "avg_monthly_demand": "sum"
    }).reset_index()

    supplier_summary.columns = ["Supplier", "# Items", "Total On Hand", "Avg Monthly Demand"]
    supplier_summary["# Items"] = supplier_summary["# Items"].astype(int)
    supplier_summary["Total On Hand"] = supplier_summary["Total On Hand"].astype(int)
    supplier_summary["Avg Monthly Demand"] = supplier_summary["Avg Monthly Demand"].astype(int)

    st.dataframe(
        supplier_summary.sort_values("# Items", ascending=False),
        use_container_width=True,
        height=300,
    )

# TAB 5: Order Proposals
with tab5:
    st.subheader("Purchase Order Proposals")

    st.info("Generate automated reorder suggestions based on current inventory levels and demand forecasts.")

    col1, col2 = st.columns([3, 1])

    with col1:
        service_level = st.slider(
            "Service Level Target",
            min_value=90,
            max_value=99,
            value=98,
            help="Target service level for safety stock calculation",
            step=1
        )

    with col2:
        if st.button("🔄 Generate Proposals", use_container_width=True):
            st.session_state.generate_proposals = True

    # Generate proposals
    proposals = []

    for _, item in items.iterrows():
        on_hand = item["on_hand"]
        avg_demand = item["avg_monthly_demand"]
        lead_time = item["lead_time_days"]
        reorder_point = item["reorder_point"]
        incoming = item["incoming_qty"]

        # Calculate reorder quantity
        available_stock = on_hand + incoming

        if available_stock < reorder_point:
            # Need to order
            qty_to_order = max(
                item["min_order_qty"],
                (reorder_point - available_stock) + (avg_demand * 3)  # 3 months of supply
            )

            proposals.append({
                "Item Code": item["item_code"],
                "Description": item["description"],
                "Current On Hand": int(on_hand),
                "Incoming": int(incoming),
                "Reorder Point": int(reorder_point),
                "Recommended Qty": int(qty_to_order),
                "Lead Time (days)": int(lead_time),
                "Supplier": item["supplier"],
                "Priority": "HIGH" if available_stock < item["safety_stock"] else "MEDIUM"
            })

    if proposals:
        proposals_df = pd.DataFrame(proposals)
        proposals_df = proposals_df.sort_values("Priority", key=lambda x: x.map({"HIGH": 0, "MEDIUM": 1}))

        st.dataframe(
            proposals_df,
            use_container_width=True,
            height=400,
            column_config={
                "Priority": st.column_config.TextColumn(width="small")
            }
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✓ Approve All", use_container_width=True):
                st.success(f"Approved {len(proposals)} purchase order proposals!")
                st.session_state.changes_log.append({
                    "timestamp": pd.Timestamp.now(),
                    "user": "Jan Koops",
                    "module": "Inventory",
                    "action": f"Approved {len(proposals)} PO proposals",
                    "before": "",
                    "after": ""
                })

        with col2:
            if st.button("📊 Export CSV", use_container_width=True):
                csv = proposals_df.to_csv(index=False)
                st.download_button(
                    label="Download Proposals",
                    data=csv,
                    file_name="po_proposals.csv",
                    mime="text/csv"
                )

        with col3:
            if st.button("⚙️ Review Settings", use_container_width=True):
                st.switch_page("pages/11_Settings.py")

    else:
        st.success("✓ All items have sufficient stock. No new orders needed at this time.")

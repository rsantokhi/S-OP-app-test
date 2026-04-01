"""PlanFlow Production Scheduling — Gantt Charts and Order Management."""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
from utils.data_loader import load_orders_out, load_item_info
from utils.styling import COLORS

st.set_page_config(page_title="Production Schedule | PlanFlow", layout="wide")

st.title("Production Scheduling")
st.markdown("Manage production workload and production schedules.")

# Load data
orders_out = load_orders_out()
items = load_item_info()

# Date range selector
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Schedule Start Date",
        value=datetime.now().date(),
        key="schedule_start"
    )

with col2:
    end_date = st.date_input(
        "Schedule End Date",
        value=(datetime.now() + timedelta(days=30)).date(),
        key="schedule_end"
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📅 Process Setup"):
        st.info("Configure production processes and resources.")

with col2:
    if st.button("🏭 Workstations"):
        st.info("Define workstations and capacities.")

with col3:
    if st.button("🤖 Auto-schedule"):
        st.success("Production schedule auto-generated!")

with col4:
    if st.button("📊 Export"):
        pass

st.divider()

# Synthetic Gantt data
workstations = ["Inbound Inspection", "Blend Cell", "Box Filler", "QA Control"]

gantt_data = []

for i, ws in enumerate(workstations):
    # Create sample tasks
    for j in range(3):
        start = start_date + timedelta(days=j*3)
        end = start + timedelta(days=2)
        gantt_data.append({
            "Task": f"Order_{j+1}",
            "Workstation": ws,
            "Start": start,
            "End": end,
            "Resource": ws,
        })

gantt_df = pd.DataFrame(gantt_data)

# Display Gantt chart
st.subheader("Production Gantt Chart")

fig = px.timeline(
    gantt_df,
    x_start="Start",
    x_end="End",
    y="Workstation",
    color="Task",
    title="Production Schedule",
    labels={
        "Workstation": "Workstation",
        "Task": "Order",
    }
)

fig.update_layout(
    height=300,
    xaxis_title="Date",
    yaxis_title="Workstation",
    hovermode="closest",
    plot_bgcolor="rgba(245,245,242,0.5)",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Orders table
st.subheader("Production Orders")

# Synthetic orders data
orders_data = []

if len(orders_out) > 0:
    for _, order in orders_out.iterrows():
        item_info = items[items["item_code"] == order["item_code"]]

        if len(item_info) > 0:
            item = item_info.iloc[0]
            orders_data.append({
                "Item Code": order["item_code"],
                "Description": item.get("description", ""),
                "Location": order.get("location", ""),
                "Quantity": int(order["quantity"]),
                "Shipment Date": order.get("shipment_date", ""),
                "Process Step": "Blend → Fill → QA",
                "Workstation": "Blend Cell",
                "Lead Time (days)": int(item.get("lead_time_days", 0)),
            })

if orders_data:
    orders_table = pd.DataFrame(orders_data)

    st.dataframe(
        orders_table,
        use_container_width=True,
        height=300,
        column_config={
            "Quantity": st.column_config.NumberColumn(format="%d"),
            "Lead Time (days)": st.column_config.NumberColumn(format="%d"),
        }
    )

else:
    st.info("No orders scheduled for this period.")

st.divider()

# Schedule details
col1, col2 = st.columns(2)

with col1:
    st.subheader("Schedule Metrics")
    st.metric("Total Orders", len(orders_data))
    st.metric("Total Units", sum([o["Quantity"] for o in orders_data]) if orders_data else 0)
    st.metric("Avg Lead Time", "5 days")

with col2:
    st.subheader("Schedule Status")
    st.info("""
    **Current Status:** On Track

    - Orders scheduled: 12
    - Workstations available: 4/4
    - Avg utilization: 78%
    - Overload days: 0
    """)

st.divider()

# Quick actions
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("+ Add Order", use_container_width=True):
        st.info("Create new production order (modal would open)")

with col2:
    if st.button("📊 View Capacity", use_container_width=True):
        st.switch_page("pages/4_Capacity.py")

with col3:
    if st.button("💾 Save Schedule", use_container_width=True):
        st.success("Schedule saved!")

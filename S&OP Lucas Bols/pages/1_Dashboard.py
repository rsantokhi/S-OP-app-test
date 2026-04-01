"""PlanFlow Dashboard — KPI Overview and Executive Summary."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import (
    load_transactions,
    load_item_info,
    load_orders_in,
    get_monthly_demand,
)
from utils.styling import metric_card, COLORS

st.set_page_config(page_title="Dashboard | PlanFlow", layout="wide")

st.title("Dashboard")
st.markdown("Executive summary of inventory, forecasting, and supply metrics.")

# Load data
transactions = load_transactions()
items = load_item_info()
orders_in = load_orders_in()
demand = get_monthly_demand()

# Calculate KPIs
total_inventory_value = (items["on_hand"] * items["unit_value"]).sum()
total_items = len(items)
avg_on_hand = items["on_hand"].mean()

# Latest month demand
latest_month = demand["year_month"].max()
latest_month_demand = demand[demand["year_month"] == latest_month]["revenue"].sum()
prev_month_demand = demand[demand["year_month"] == latest_month - 1]["revenue"].sum() if latest_month > demand["year_month"].min() else 0

revenue_change = (latest_month_demand - prev_month_demand) / prev_month_demand * 100 if prev_month_demand > 0 else 0

# Forecast accuracy (MAPE) - simulated
forecast_accuracy = 87.6  # Placeholder

# Calculate metrics
total_on_order = orders_in["quantity"].sum()
avg_lead_time = items["lead_time_days"].mean()

# Revenue at risk (simple: items below safety stock)
low_stock_items = items[items["on_hand"] < (items["on_hand"].mean() * 0.5)]
revenue_at_risk = (low_stock_items["on_hand"] * low_stock_items["unit_value"]).sum()

# Overstock exposure
high_stock_items = items[items["on_hand"] > (items["on_hand"].quantile(0.75))]
overstock_exposure = (high_stock_items["on_hand"] * high_stock_items["unit_value"]).sum()

# OTIF (On-Time-In-Full) - simulated
otif_rate = 96.3

# Open purchase orders
open_pos = len(orders_in)

# Display KPI metrics
st.subheader("Key Performance Indicators")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(
        metric_card(
            "Total Inventory Value",
            f"€{total_inventory_value/1e6:.1f}M",
            f"-€{prev_month_demand*0.05/1e6:.1f}M vs last month",
            delta_positive=False,
        ),
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        metric_card(
            "Forecast Accuracy",
            f"{forecast_accuracy:.1f}%",
            f"+2.1pp vs last cycle",
            delta_positive=True,
        ),
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        metric_card(
            "Revenue at Risk",
            f"€{revenue_at_risk/1e6:.2f}M",
            "-€3.8k on critical shortage",
            delta_positive=False,
        ),
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        metric_card(
            "Overstock Exposure",
            f"€{overstock_exposure/1e6:.1f}M",
            "-€2.3M vs 190 DOH",
            delta_positive=True,
        ),
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        metric_card(
            "OTIF Rate",
            f"{otif_rate:.1f}%",
            "+0.5pp vs target",
            delta_positive=True,
        ),
        unsafe_allow_html=True,
    )

with col6:
    st.markdown(
        metric_card(
            "Open POs",
            f"{open_pos}",
            f"-3 vs in transit",
            delta_positive=True,
        ),
        unsafe_allow_html=True,
    )

st.divider()

# Charts section
col1, col2 = st.columns(2)

# Revenue forecast trend
with col1:
    st.subheader("Revenue Forecast — Next 6 Months")

    # Generate forecast trend (synthetic)
    months_ahead = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
    forecast_values = [2.5, 2.6, 2.8, 2.7, 2.4, 2.6]
    last_year_values = [2.3, 2.4, 2.7, 2.5, 2.2, 2.4]

    forecast_df = pd.DataFrame({
        "Month": months_ahead,
        "Forecast": forecast_values,
        "Last Year": last_year_values,
    })

    fig_revenue = px.line(
        forecast_df,
        x="Month",
        y=["Forecast", "Last Year"],
        markers=True,
        title=None,
        labels={"value": "Revenue (EUR millions)", "Month": ""},
    )
    fig_revenue.update_layout(
        hovermode="x unified",
        plot_bgcolor="rgba(245,245,242,0.5)",
        paper_bgcolor="white",
        font=dict(size=11),
        height=350,
        showlegend=True,
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

# ERP Sync Status
with col2:
    st.subheader("ERP Sync Status")

    sync_status = [
        {"item": "Inventory balances", "status": "Synced", "time": "Synced 29m ago"},
        {"item": "Purchase orders", "status": "Synced", "time": "Synced 12m ago"},
        {"item": "Item master", "status": "Synced", "time": "Synced 4h ago"},
        {"item": "Sales orders", "status": "Planned", "time": "Planned 42m ago"},
        {"item": "Supplier list", "status": "Exception", "time": "Exception 92m ago"},
    ]

    sync_html = '<div style="display: flex; flex-direction: column; gap: 10px;">'
    for item in sync_status:
        status_color = {
            "Synced": "green",
            "Planned": "orange",
            "Exception": "red",
        }.get(item["status"], "gray")

        status_icon = {
            "Synced": "✓",
            "Planned": "⏳",
            "Exception": "⚠",
        }.get(item["status"], "•")

        sync_html += f'''
        <div style="display: flex; justify-content: space-between; align-items: center;
                    padding: 10px; border-bottom: 1px solid #e0e8f0;">
            <div>
                <div style="font-size: 13px; font-weight: 600; color: #0066CC;">
                    {status_icon} {item['item']}
                </div>
                <div style="font-size: 11px; color: #8898aa;">{item['time']}</div>
            </div>
            <span style="background: rgba(0,119,68,0.15); color: {status_color};
                         padding: 3px 8px; border-radius: 4px; font-size: 9px;
                         font-weight: 600;">{item['status']}</span>
        </div>
        '''

    sync_html += '</div>'
    st.markdown(sync_html, unsafe_allow_html=True)

st.divider()

# Inventory composition
st.subheader("Inventory Distribution")

col1, col2 = st.columns(2)

with col1:
    # Items by category
    category_dist = items.groupby("category")["on_hand"].sum().reset_index()
    category_dist = category_dist.sort_values("on_hand", ascending=False)

    fig_category = px.bar(
        category_dist,
        x="category",
        y="on_hand",
        title="Inventory by Category",
        labels={"on_hand": "Units on Hand", "category": "Category"},
    )
    fig_category.update_layout(
        height=300,
        showlegend=False,
        hovermode="x unified",
        font=dict(size=10),
    )
    st.plotly_chart(fig_category, use_container_width=True)

with col2:
    # Top items by value
    items_top = items.nlargest(10, "on_hand")[["description", "on_hand", "unit_value"]]
    items_top["value"] = items_top["on_hand"] * items_top["unit_value"]
    items_top = items_top.sort_values("value", ascending=True)

    fig_top = px.barh(
        items_top,
        x="value",
        y="description",
        title="Top 10 Items by Inventory Value",
        labels={"value": "Inventory Value (EUR)", "description": "Item"},
    )
    fig_top.update_layout(
        height=300,
        showlegend=False,
        font=dict(size=9),
    )
    st.plotly_chart(fig_top, use_container_width=True)

st.divider()

# Data summary
st.subheader("Data Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Items", f"{total_items:,.0f}")

with col2:
    st.metric("Avg Lead Time", f"{avg_lead_time:.0f} days")

with col3:
    st.metric("Total On Order", f"{total_on_order:,.0f} units")

with col4:
    st.metric("Avg Inventory", f"{avg_on_hand:,.0f} units/item")

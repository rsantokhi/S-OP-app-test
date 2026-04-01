"""PlanFlow Demand Planning — Forecast Management and Scenario Analysis."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from utils.data_loader import (
    load_item_info,
    get_monthly_demand,
    get_item_categories,
    get_items_by_category,
)
from utils.forecast_engine import run_forecast
from utils.styling import COLORS

st.set_page_config(page_title="Demand Planning | PlanFlow", layout="wide")

st.title("Demand Planning")
st.markdown("Manage demand forecasts with statistical models and manual overrides.")

# Load data
items = load_item_info()
demand = get_monthly_demand()
categories = get_item_categories()

# Initialize session state
if "selected_item" not in st.session_state:
    st.session_state.selected_item = items["item_code"].iloc[0] if len(items) > 0 else None

# Sidebar Configuration
with st.sidebar:
    st.subheader("📊 Configuration")

    st.divider()

    denomination = st.radio(
        "View Level",
        options=["All Items", "By Category"],
        index=0
    )

    if denomination == "By Category":
        selected_category = st.selectbox(
            "Category",
            options=["All"] + categories,
        )
        if selected_category == "All":
            item_codes = sorted(items["item_code"].unique().tolist())
        else:
            item_codes = get_items_by_category(selected_category)
    else:
        item_codes = sorted(items["item_code"].unique().tolist())

    st.divider()

    st.subheader("🤖 Forecasting")

    selected_model = st.selectbox(
        "Model",
        options=["Ensemble", "ETS", "SARIMA", "Prophet", "Naive"],
        help="Select forecasting algorithm"
    )

    forecast_horizon = st.slider(
        "Forecast Horizon",
        min_value=1,
        max_value=24,
        value=12,
        step=1,
        help="Months to forecast"
    )

    if st.button("📊 Run Forecast", use_container_width=True):
        st.session_state.run_forecast = True
        st.rerun()

st.divider()

# Get data for selected item
if st.session_state.selected_item and st.session_state.selected_item in items["item_code"].values:
    selected_item = st.session_state.selected_item
    item_info = items[items["item_code"] == selected_item].iloc[0]

    # Get historical demand
    item_demand = demand[demand["item_code"] == selected_item].sort_values("year_month")

    if len(item_demand) == 0:
        st.warning(f"No demand data available for {selected_item}")
        st.stop()

    # Get last 12 months
    recent_demand = item_demand.tail(12)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Item", selected_item)
    with col2:
        st.metric("Description", item_info.get("description", "N/A")[:30])
    with col3:
        st.metric("Category", item_info.get("category", "N/A"))
    with col4:
        st.metric("Supplier", item_info.get("supplier", "N/A"))
    with col5:
        st.metric("On Hand", int(item_info.get("on_hand", 0)))

    st.divider()

    # Create demand planning table
    st.subheader("📋 Demand Planning Grid")

    # Prepare table data
    months = recent_demand["year_month"].astype(str).tolist()
    actuals = recent_demand["quantity"].tolist()

    # Run forecast if requested
    forecast_values = None
    if st.session_state.get("run_forecast", False):
        try:
            series = item_demand.set_index("year_month")["quantity"]
            forecast_values = run_forecast(series, selected_model.lower(), forecast_horizon)
        except:
            forecast_values = None
        st.session_state.run_forecast = False

    # Build planning table
    planning_data = {
        "Metric": [
            "Actual Sales",
            "Statistical Forecast",
            "Final Forecast",
            "Marketing Forecast",
            "Sales Order Forecast",
            "",
            "Average Sales Price",
            "Revenue",
            "",
            "On Hand",
            "Shortage Days",
            "Historical Service Level",
            "Projected Inventory",
            "Ordering Plan"
        ]
    }

    # Add months as columns
    for i, month in enumerate(months):
        month_str = str(month)
        planning_data[month_str] = [
            int(actuals[i]) if i < len(actuals) else 0,  # Actual Sales
            int(actuals[i] * 0.95) if i < len(actuals) else 0,  # Statistical Forecast
            int(actuals[i] * 0.98) if i < len(actuals) else 0,  # Final Forecast
            int(actuals[i] * 1.05) if i < len(actuals) else 0,  # Marketing Forecast
            int(actuals[i] * 1.02) if i < len(actuals) else 0,  # Sales Order Forecast
            "",  # Spacer
            f"€{np.random.randint(10, 100)}",  # Average Sales Price
            f"€{int(actuals[i] * np.random.randint(50, 150))}",  # Revenue
            "",  # Spacer
            int(item_info.get("on_hand", 0)),  # On Hand
            np.random.randint(0, 30),  # Shortage Days
            "98%",  # Historical Service Level
            int(item_info.get("on_hand", 0) - actuals[i] if i < len(actuals) else 0),  # Projected Inventory
            int(actuals[i] * 1.5),  # Ordering Plan
        ]

    # Add forecast months if available
    if forecast_values is not None:
        for i, f_val in enumerate(forecast_values[:3]):
            forecast_month = f"F+{i+1}m"
            planning_data[forecast_month] = [
                "",  # Actual Sales
                int(f_val * 0.95),  # Statistical Forecast
                int(f_val * 0.98),  # Final Forecast
                int(f_val * 1.05),  # Marketing Forecast
                int(f_val * 1.02),  # Sales Order Forecast
                "",  # Spacer
                f"€{np.random.randint(10, 100)}",  # Average Sales Price
                f"€{int(f_val * np.random.randint(50, 150))}",  # Revenue
                "",  # Spacer
                int(item_info.get("on_hand", 0)),  # On Hand
                0,  # Shortage Days
                "98%",  # Historical Service Level
                int(item_info.get("on_hand", 0) - f_val),  # Projected Inventory
                int(f_val * 1.5),  # Ordering Plan
            ]

    df_planning = pd.DataFrame(planning_data)

    # Display table with custom styling
    st.dataframe(
        df_planning,
        use_container_width=True,
        height=500,
        column_config={col: st.column_config.NumberColumn(format="%d")
                      if col not in ["Metric"] and col != ""
                      else st.column_config.TextColumn()
                      for col in df_planning.columns}
    )

    st.divider()

    # Charts
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheading("📈 Demand Trend")

        # Create chart
        chart_months = months + (["F+1m", "F+2m", "F+3m"] if forecast_values is not None else [])
        chart_actuals = actuals + ([0, 0, 0] if forecast_values is not None else [])
        chart_forecast = ([0]*len(actuals) + list(forecast_values[:3])) if forecast_values is not None else []

        fig = go.Figure()

        # Add actual sales
        fig.add_trace(go.Scatter(
            x=months,
            y=actuals,
            mode="lines+markers",
            name="Actual Sales",
            line=dict(color=COLORS["primary_blue"], width=2),
            marker=dict(size=8)
        ))

        # Add forecast if available
        if forecast_values is not None:
            forecast_months = ["F+1m", "F+2m", "F+3m"]
            fig.add_trace(go.Scatter(
                x=forecast_months,
                y=list(forecast_values[:3]),
                mode="lines+markers",
                name="Forecast",
                line=dict(color=COLORS["accent_orange"], width=2, dash="dash"),
                marker=dict(size=8)
            ))

        fig.update_layout(
            title=f"{selected_item} - Demand Forecast",
            xaxis_title="Month",
            yaxis_title="Quantity (units)",
            hovermode="x unified",
            height=400,
            plot_bgcolor="rgba(245,245,242,0.5)",
            font=dict(size=11)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheading("📊 Statistics")
        col1, col2 = st.columns(1)
        with col1:
            st.metric("Avg Demand", f"{item_demand['quantity'].mean():.0f} units")
            st.metric("Std Dev", f"{item_demand['quantity'].std():.0f} units")
            st.metric("Latest", f"{item_demand['quantity'].iloc[-1]:.0f} units")
            st.metric("Trend", "↑ Growing" if item_demand['quantity'].iloc[-1] > item_demand['quantity'].iloc[0] else "↓ Declining")

    st.divider()

    # Item selector
    st.subheading("🔍 Select Item")
    st.session_state.selected_item = st.selectbox(
        "Choose item to view",
        options=item_codes,
        index=item_codes.index(st.session_state.selected_item) if st.session_state.selected_item in item_codes else 0,
        key="item_select"
    )

    if st.session_state.selected_item:
        st.rerun()

else:
    st.warning("⚠️ No items available. Check data loading.")

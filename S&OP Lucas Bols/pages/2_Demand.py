"""PlanFlow Demand Planning — Forecast Management and Scenario Analysis."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.data_loader import (
    load_item_info,
    get_monthly_demand,
    get_item_categories,
    get_items_by_category,
)
from utils.forecast_engine import run_forecast, run_ensemble
from utils.styling import COLORS

st.set_page_config(page_title="Demand Planning | PlanFlow", layout="wide")

st.title("Demand Planning")
st.markdown("Manage demand forecasts with statistical and manual overrides.")

# Load data
items = load_item_info()
demand = get_monthly_demand()
categories = get_item_categories()

# Sidebar configuration
with st.sidebar:
    st.subheader("Configuration")

    denomination_plan = st.selectbox(
        "Denomination Plan",
        options=["All", "By Channel", "By Category"],
        help="Grouping level for forecast"
    )

    selected_category = st.selectbox(
        "Item Category",
        options=["All"] + categories,
        help="Filter items by category"
    )

    price_controlled = st.checkbox(
        "Price Controlled Only",
        value=False,
        help="Show only price-controlled items"
    )

    st.divider()

    st.subheader("Forecasting Panel")
    selected_model = st.selectbox(
        "Forecast Model",
        options=["Ensemble", "ETS", "SARIMA", "Prophet", "Naive"],
        help="Select forecasting algorithm"
    )

    forecast_horizon = st.number_input(
        "Forecast Horizon (months)",
        min_value=1,
        max_value=24,
        value=st.session_state.settings["forecast_horizon"],
        step=1
    )

    if st.button("📊 Run Forecast", use_container_width=True):
        st.session_state.run_forecast = True
        st.rerun()

# Filter items based on selection
if selected_category == "All":
    item_codes = sorted(items["item_code"].unique().tolist())
else:
    item_codes = get_items_by_category(selected_category)

# Get monthly periods for columns
all_periods = sorted(demand["year_month"].unique().tolist())
recent_periods = all_periods[-24:]  # Last 24 months

# Create demand pivot table
demand_pivot = demand[demand["year_month"].isin(recent_periods)].pivot_table(
    index="item_code",
    columns="year_month",
    values="quantity",
    aggfunc="sum",
    fill_value=0
)

# Add forecast columns
forecast_periods = []
if all_periods:
    last_period = all_periods[-1]
    # Generate next 12 forecast periods
    for i in range(1, forecast_horizon + 1):
        forecast_periods.append(f"Forecast_{i}m")

# Build the planning table
st.subheader("Demand Forecast by Item")

# Prepare table data
table_data = []

for item_code in item_codes:
    item_info = items[items["item_code"] == item_code].iloc[0] if len(items[items["item_code"] == item_code]) > 0 else None

    if item_info is None:
        continue

    row = {"Item": item_code, "Description": item_info.get("description", "")}

    # Add historical quantities
    for period in recent_periods[-12:]:  # Last 12 months
        col_name = str(period)
        value = demand_pivot.loc[item_code, period] if item_code in demand_pivot.index and period in demand_pivot.columns else 0
        row[col_name] = int(value)

    # Add forecast
    if st.session_state.get("run_forecast", False):
        # Get historical series for this item
        item_demand = demand[demand["item_code"] == item_code].sort_values("year_month")

        if len(item_demand) > 0:
            series = item_demand.set_index("year_month")["quantity"]
            try:
                forecast = run_forecast(series, selected_model.lower(), forecast_horizon)
                for i, f_val in enumerate(forecast[:3]):  # Show first 3 forecast months
                    row[f"F_{i+1}"] = int(f_val)
            except:
                pass

    # Add on-hand quantity
    row["On Hand"] = int(item_info.get("on_hand", 0))

    table_data.append(row)

# Display table
if table_data:
    df_display = pd.DataFrame(table_data[:20])  # Show first 20 items

    st.dataframe(
        df_display,
        use_container_width=True,
        height=400,
        column_config={
            col: st.column_config.NumberColumn(format="%d") for col in df_display.columns if col not in ["Item", "Description"]
        }
    )

st.divider()

# Forecast comparison chart
st.subheader("Forecast Visualization")

col1, col2 = st.columns([3, 1])

with col1:
    selected_item = st.selectbox(
        "Select Item to Visualize",
        options=item_codes,
        key="chart_item_select"
    )

    if selected_item:
        item_demand = demand[demand["item_code"] == selected_item].sort_values("year_month")

        if len(item_demand) > 0:
            # Historical data
            historical_months = item_demand["year_month"].astype(str).tolist()
            historical_values = item_demand["quantity"].tolist()

            # Generate forecast
            series = item_demand.set_index("year_month")["quantity"]
            try:
                forecast = run_forecast(series, selected_model.lower(), forecast_horizon)
                forecast_months = [f"F+{i+1}" for i in range(len(forecast))]
            except:
                forecast = []
                forecast_months = []

            # Create figure
            fig = go.Figure()

            # Add historical line
            fig.add_trace(go.Scatter(
                x=historical_months,
                y=historical_values,
                mode="lines+markers",
                name="Actual",
                line=dict(color=COLORS["primary_blue"], width=2),
                marker=dict(size=6),
            ))

            # Add forecast line
            if forecast:
                fig.add_trace(go.Scatter(
                    x=forecast_months,
                    y=forecast,
                    mode="lines+markers",
                    name="Forecast",
                    line=dict(color=COLORS["accent_orange"], width=2, dash="dash"),
                    marker=dict(size=6),
                ))

            fig.update_layout(
                title=f"{selected_item} — Demand Forecast",
                xaxis_title="Period",
                yaxis_title="Quantity",
                hovermode="x unified",
                plot_bgcolor="rgba(245,245,242,0.5)",
                height=350,
                font=dict(size=11),
            )

            st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Stats")
    if len(item_demand) > 0:
        st.metric("Avg Demand", f"{item_demand['quantity'].mean():.0f} units")
        st.metric("Std Dev", f"{item_demand['quantity'].std():.0f} units")
        st.metric("Latest Month", f"{item_demand['quantity'].iloc[-1]:.0f} units")

st.divider()

# Forecasting details
st.subheader("Forecasting Configuration")

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    **Selected Model:** {selected_model}

    - **ETS:** Exponential smoothing with trend and seasonality
    - **SARIMA:** Auto-selected ARIMA with seasonal patterns
    - **Prophet:** Facebook's time-series library (handles holidays)
    - **Naive:** Same-month-last-year baseline
    - **Ensemble:** Weighted average of all models by accuracy
    """)

with col2:
    st.info(f"""
    **Forecast Horizon:** {forecast_horizon} months

    Recent settings:
    - Seasonal threshold: {st.session_state.settings['seasonal_threshold']}
    - Outlier correction: {st.session_state.settings['outlier_correction']}
    - Demand sensing: {st.session_state.settings['demand_sensing']}

    Adjust in Settings page.
    """)

st.divider()

# Save configuration
if st.button("💾 Save Forecast Overrides", use_container_width=True):
    st.session_state.settings["forecast_horizon"] = forecast_horizon
    st.success("Forecast settings saved!")

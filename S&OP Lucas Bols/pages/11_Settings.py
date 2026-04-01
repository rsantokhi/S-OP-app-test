"""PlanFlow Settings — Configuration and Parameters."""

import streamlit as st

st.set_page_config(page_title="Settings | PlanFlow", layout="wide")

st.title("Settings")
st.markdown("Configure forecasting and inventory parameters.")

# Tabs for settings sections
tab1, tab2, tab3 = st.tabs(["Forecast Settings", "Inventory Settings", "System Settings"])

# TAB 1: Forecast Settings
with tab1:
    st.subheader("Forecast Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Forecasting Algorithm:**")

        horizon = st.number_input(
            "Forecast Horizon (months)",
            min_value=1,
            max_value=36,
            value=st.session_state.settings["forecast_horizon"],
            step=1,
            help="Number of months to forecast ahead"
        )

        seasonal_threshold = st.number_input(
            "Seasonal Threshold (score)",
            min_value=0,
            max_value=10,
            value=st.session_state.settings["seasonal_threshold"],
            step=1,
            help="Minimum score to identify seasonal pattern"
        )

        promotion_threshold = st.number_input(
            "Promotion Detection Threshold",
            min_value=0,
            max_value=100,
            value=st.session_state.settings["promotion_threshold"],
            step=5,
            help="% increase to flag as promotion"
        )

    with col2:
        st.write("**Forecast Options:**")

        top_down_default = st.radio(
            "Top-Down Forecast Default",
            options=["None", "Brand", "Category"],
            index=["None", "Brand", "Category"].index(st.session_state.settings["top_down_default"]),
            help="Default grouping for top-down reconciliation"
        )

        revenue_basis = st.radio(
            "Revenue Calculation Basis",
            options=["Final Forecast", "Sales Order"],
            index=["Final Forecast", "Sales Order"].index(st.session_state.settings["revenue_basis"]),
            help="Which forecast to use for top-line revenue"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        outlier_correction = st.checkbox(
            "Automatic Outlier Correction",
            value=st.session_state.settings["outlier_correction"],
            help="Enable automatic outlier detection and removal"
        )

    with col2:
        demand_sensing = st.checkbox(
            "Demand Sensing",
            value=st.session_state.settings["demand_sensing"],
            help="Enable demand sensing for near-term forecast adjustment"
        )

    st.info("""
    **About Demand Sensing:**
    Demand sensing opens the near-term forecast (next 2 weeks) to adjustment based on
    real-time signals (point-of-sale, web traffic, supply chain signals). Improves short-term
    accuracy but requires real-time data integration.
    """)

# TAB 2: Inventory Settings
with tab2:
    st.subheader("Inventory Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Defaults:**")

        default_lead_time = st.number_input(
            "Default Lead Time (days)",
            min_value=1,
            max_value=365,
            value=st.session_state.settings["default_lead_time"],
            step=1,
            help="Default supplier lead time when not specified"
        )

        default_order_cycle = st.number_input(
            "Default Order Cycle (days)",
            min_value=1,
            max_value=365,
            value=st.session_state.settings["default_order_cycle"],
            step=1,
            help="Default ordering frequency"
        )

    with col2:
        st.write("**Safety Stock:**")

        service_level = st.slider(
            "Service Level Target",
            min_value=80,
            max_value=99,
            value=98,
            step=1,
            help="Target service level for safety stock calculation"
        )

        safety_stock_method = st.radio(
            "Safety Stock Method",
            options=["Standard (Z-score)", "Percentile", "Min-Max"],
            index=0,
            help="Method for calculating safety stock"
        )

    st.divider()

    st.write("**Reordering Rules:**")

    col1, col2, col3 = st.columns(3)

    with col1:
        min_order_qty = st.number_input(
            "Minimum Order Quantity",
            min_value=1,
            max_value=10000,
            value=100,
            step=10
        )

    with col2:
        order_rounding = st.number_input(
            "Order Rounding (units)",
            min_value=1,
            max_value=10000,
            value=50,
            step=10,
            help="Round order quantities to nearest value"
        )

    with col3:
        target_days_inventory = st.number_input(
            "Target Days Inventory",
            min_value=1,
            max_value=180,
            value=45,
            step=5
        )

# TAB 3: System Settings
with tab3:
    st.subheader("System Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Data Sync:**")

        auto_sync = st.checkbox(
            "Enable Automatic Sync",
            value=True,
            help="Auto-sync with Oracle Fusion and other systems"
        )

        sync_frequency = st.selectbox(
            "Sync Frequency",
            options=["Real-time", "Hourly", "Daily", "Weekly"],
            index=1,
            help="How often to sync with source systems"
        )

    with col2:
        st.write("**Notifications:**")

        email_alerts = st.checkbox(
            "Email Alerts",
            value=True,
            help="Send email notifications for critical exceptions"
        )

        alert_threshold = st.number_input(
            "Alert Threshold (EUR)",
            min_value=0,
            max_value=1000000,
            value=10000,
            step=1000,
            help="Minimum exception value to trigger alert"
        )

    st.divider()

    st.write("**Data Retention:**")

    col1, col2, col3 = st.columns(3)

    with col1:
        retention_months = st.number_input(
            "Retention Period (months)",
            min_value=1,
            max_value=120,
            value=36,
            help="Keep historical data for this many months"
        )

    with col2:
        archive_old_data = st.checkbox(
            "Archive Old Data",
            value=True,
            help="Archive data older than retention period"
        )

    with col3:
        backup_frequency = st.selectbox(
            "Backup Frequency",
            options=["Daily", "Weekly", "Monthly"],
            index=0
        )

st.divider()

# Save settings
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.write("")  # Spacer

with col2:
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        st.session_state.settings = {
            "forecast_horizon": 12,
            "seasonal_threshold": 8,
            "promotion_threshold": 8,
            "top_down_default": "None",
            "revenue_basis": "Final Forecast",
            "outlier_correction": True,
            "demand_sensing": True,
            "default_lead_time": 30,
            "default_order_cycle": 7,
        }
        st.success("✓ Settings reset to defaults")

with col3:
    if st.button("💾 Save Settings", use_container_width=True):
        # Save all settings to session state
        st.session_state.settings["forecast_horizon"] = horizon
        st.session_state.settings["seasonal_threshold"] = seasonal_threshold
        st.session_state.settings["promotion_threshold"] = promotion_threshold
        st.session_state.settings["top_down_default"] = top_down_default
        st.session_state.settings["revenue_basis"] = revenue_basis
        st.session_state.settings["outlier_correction"] = outlier_correction
        st.session_state.settings["demand_sensing"] = demand_sensing
        st.session_state.settings["default_lead_time"] = default_lead_time
        st.session_state.settings["default_order_cycle"] = default_order_cycle

        st.success("✓ Settings saved!")
        st.balloons()

st.divider()

# Info section
st.info("""
**About PlanFlow Settings:**

These settings control the behavior of the forecasting engine, inventory management,
and system integration. Changes take effect immediately for new forecasts and plans.

For detailed documentation, visit: **[PlanFlow Docs](https://docs.planflow.nl)**
""")

"""PlanFlow — S&OP Planning Application for Lucas Bols."""

import streamlit as st
from utils.styling import inject_css, COLORS, badge

# Configure Streamlit page
st.set_page_config(
    page_title="PlanFlow | S&OP Planning",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom styling
inject_css()

# Initialize session state
if "settings" not in st.session_state:
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

if "changes_log" not in st.session_state:
    st.session_state.changes_log = []

if "forecast_overrides" not in st.session_state:
    st.session_state.forecast_overrides = {}

if "promotions" not in st.session_state:
    st.session_state.promotions = []

if "new_products" not in st.session_state:
    st.session_state.new_products = []

if "approvals" not in st.session_state:
    st.session_state.approvals = []

if "saop_cycle" not in st.session_state:
    st.session_state.saop_cycle = {
        "name": "April 2025",
        "lock_date": "2025-04-21",
        "forecast_status": "Submitted",
        "supply_review": "In progress",
        "exec_approval": "Pending",
    }


# Custom sidebar
with st.sidebar:
    # Logo / Branding
    st.markdown(
        f"""
        <div style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid {COLORS['border']};">
            <div style="font-size: 24px; font-weight: 700; color: {COLORS['primary_blue']}; margin-bottom: 4px;">
                Plan<span style="font-weight: 300;">Flow</span>
            </div>
            <div style="font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: {COLORS['text_tertiary']};">
                S&OP Planning
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # PLANNING Section
    st.markdown(
        '<div class="nav-section">📋 Planning</div>',
        unsafe_allow_html=True,
    )
    if st.page_link("pages/1_Dashboard.py", label="📊 Dashboard"):
        pass
    if st.page_link("pages/2_Demand.py", label="📈 Demand"):
        pass
    if st.page_link("pages/3_Inventory.py", label="📦 Inventory"):
        pass
    if st.page_link("pages/4_Capacity.py", label="⚙️ Capacity"):
        pass
    if st.page_link("pages/5_Schedule.py", label="📅 Schedule"):
        pass

    # ANALYSIS Section
    st.markdown(
        '<div class="nav-section">📊 Analysis</div>',
        unsafe_allow_html=True,
    )
    if st.page_link("pages/1_Dashboard.py", label="📈 Reports"):
        pass

    # WORKFLOW Section
    st.markdown(
        '<div class="nav-section">🔄 Workflow</div>',
        unsafe_allow_html=True,
    )
    if st.page_link("pages/6_SOP_Review.py", label="S&OP Review"):
        pass

    approvals_count = len([a for a in st.session_state.approvals if a.get("status") == "pending"])
    approval_label = f"Approvals {badge(str(approvals_count), 'orange', approvals_count) if approvals_count > 0 else ''}"
    if st.page_link("pages/7_Approvals.py", label="Approvals"):
        pass

    if st.page_link("pages/8_Promo_Planning.py", label="Promo Planning"):
        pass
    if st.page_link("pages/9_New_Products.py", label="New Products"):
        pass
    if st.page_link("pages/10_Changes_Log.py", label="Changes Log"):
        pass

    # SYSTEM Section
    st.markdown(
        '<div class="nav-section">⚙️ System</div>',
        unsafe_allow_html=True,
    )
    if st.page_link("pages/11_Settings.py", label="Settings"):
        pass

    # Footer / User
    st.markdown(
        f"""
        <div style="position: fixed; bottom: 20px; left: 20px; right: 20px;
                    display: flex; align-items: center; gap: 10px;
                    padding-top: 12px; border-top: 1px solid {COLORS['border']};">
            <div style="width: 32px; height: 32px; border-radius: 50%;
                        background: {COLORS['primary_blue']}; color: white;
                        display: flex; align-items: center; justify-content: center;
                        font-size: 12px; font-weight: 600;">JK</div>
            <div>
                <div style="font-size: 12px; font-weight: 600; color: {COLORS['text_primary']};">Jan Koops</div>
                <div style="font-size: 10px; color: {COLORS['text_tertiary']};">S&OP Planner</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Main content area
st.title("PlanFlow — Sales & Operations Planning")

st.markdown(
    f"""
    Welcome to **PlanFlow**, your integrated demand and supply planning platform for Lucas Bols.

    Select a module from the sidebar to get started. Use the **Demand Planning** module to manage forecasts,
    **Inventory** for supply management, and **S&OP Review** to monitor your planning cycle.
    """,
)

# Show current cycle status
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Cycle", st.session_state.saop_cycle["name"])
with col2:
    st.metric("Forecast Status", st.session_state.saop_cycle["forecast_status"])
with col3:
    st.metric("Supply Review", st.session_state.saop_cycle["supply_review"])
with col4:
    st.metric("Exec Approval", st.session_state.saop_cycle["exec_approval"])

st.divider()

# Quick links
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📈 Go to Demand Planning", use_container_width=True):
        st.switch_page("pages/2_Demand.py")
with col2:
    if st.button("📦 Go to Inventory", use_container_width=True):
        st.switch_page("pages/3_Inventory.py")
with col3:
    if st.button("📊 Go to Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

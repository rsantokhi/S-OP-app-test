"""PlanFlow S&OP Review — Planning Cycle Management and Approvals."""

import streamlit as st
import pandas as pd
from utils.styling import COLORS, badge

st.set_page_config(page_title="S&OP Review | PlanFlow", layout="wide")

st.title("S&OP Review")
st.markdown("Monitor and manage Sales & Operations Planning cycles.")

# Get current cycle from session
cycle = st.session_state.saop_cycle

# Cycle status header
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background: white; border: 1px solid #e0e8f0; border-radius: 8px; padding: 12px;">
        <div style="font-size: 11px; color: #8898aa; text-transform: uppercase; letter-spacing: 1px;">Cycle</div>
        <div style="font-size: 16px; font-weight: 700; color: #0066CC; margin-top: 4px;">
            {cycle['name']}
        </div>
        <div style="font-size: 10px; color: #8898aa; margin-top: 4px;">
            Lock date: {cycle['lock_date']}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    status_color = "green" if cycle['forecast_status'] == "Submitted" else "orange"
    st.markdown(f"""
    <div style="background: white; border: 1px solid #e0e8f0; border-radius: 8px; padding: 12px;">
        <div style="font-size: 11px; color: #8898aa; text-transform: uppercase; letter-spacing: 1px;">Forecast Status</div>
        <div style="font-size: 16px; font-weight: 700; color: #0066CC; margin-top: 4px;">
            {cycle['forecast_status']}
        </div>
        <div style="font-size: 10px; color: #8898aa; margin-top: 4px;">
            By Jan Koops 29 ago
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: white; border: 1px solid #e0e8f0; border-radius: 8px; padding: 12px;">
        <div style="font-size: 11px; color: #8898aa; text-transform: uppercase; letter-spacing: 1px;">Supply Review</div>
        <div style="font-size: 16px; font-weight: 700; color: #0066CC; margin-top: 4px;">
            {cycle['supply_review']}
        </div>
        <div style="font-size: 10px; color: #8898aa; margin-top: 4px;">
            Awaiting supply input
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background: white; border: 1px solid #e0e8f0; border-radius: 8px; padding: 12px;">
        <div style="font-size: 11px; color: #8898aa; text-transform: uppercase; letter-spacing: 1px;">Exec Approval</div>
        <div style="font-size: 16px; font-weight: 700; color: #0066CC; margin-top: 4px;">
            {cycle['exec_approval']}
        </div>
        <div style="font-size: 10px; color: #8898aa; margin-top: 4px;">
            Awaiting mgmt. approval
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Summary KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Forecast Accuracy", "87.6%", "+4.1pp vs last cycle")

with col2:
    st.metric("Total Demand", "€87.4M", "-4.3% vs plan")

with col3:
    st.metric("Inventory Cover", "38 days", "+2 days to plan")

with col4:
    st.metric("Open Exceptions", "7", "Requires action today")

st.divider()

# Exceptions table
st.subheader("Open Exceptions")

exceptions_data = [
    {
        "ID": "BOL.ELW713",
        "Type": "Shortage",
        "Description": "Elderflower B.V. — stockout risk Jan 29",
        "Impact": "€348.5k",
        "Owner": "Jan Koops",
        "Status": "⚠️ Action needed",
    },
    {
        "ID": "BOL.ELM713",
        "Type": "Overstock",
        "Description": "Jan Autumn D.S. — 1,180 BOC in warehouse",
        "Impact": "€125.3k",
        "Owner": "Jan Koops",
        "Status": "📋 Pending",
    },
    {
        "ID": "BOL.GLI0000",
        "Type": "Overstock",
        "Description": "Galliano Vanilla EXTRA — excess stock Q2",
        "Impact": "€411.4k",
        "Owner": "Jan Frost",
        "Status": "📋 Pending",
    },
    {
        "ID": "BOL.CAP026",
        "Type": "Capacity",
        "Description": "Finished Products line — 110% load Aug 2025",
        "Impact": "-€47.7k",
        "Owner": "Ops team",
        "Status": "🔴 Critical",
    },
    {
        "ID": "BOL.NEW001",
        "Type": "Shortage",
        "Description": "New product ramp-up demand exceeding forecast",
        "Impact": "€89.2k",
        "Owner": "Marketing",
        "Status": "⚠️ Action needed",
    },
    {
        "ID": "BOL.SUP002",
        "Type": "Supply",
        "Description": "Supplier delay on key components",
        "Impact": "€156.8k",
        "Owner": "Procurement",
        "Status": "⚠️ Action needed",
    },
    {
        "ID": "BOL.FOR001",
        "Type": "Forecast",
        "Description": "Model accuracy below threshold for SKU-123",
        "Impact": "€42.1k",
        "Owner": "Jan Koops",
        "Status": "📋 Pending",
    },
]

exceptions_df = pd.DataFrame(exceptions_data)

st.dataframe(
    exceptions_df,
    use_container_width=True,
    height=400,
    column_config={
        "ID": st.column_config.TextColumn(width="small"),
        "Type": st.column_config.TextColumn(width="small"),
        "Impact": st.column_config.TextColumn(width="small"),
        "Owner": st.column_config.TextColumn(width="small"),
    }
)

st.divider()

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.write("")  # Spacer

with col2:
    if st.button("📥 Export Meeting Pack", use_container_width=True):
        # Generate CSV
        csv = exceptions_df.to_csv(index=False)
        st.download_button(
            label="Download Exceptions",
            data=csv,
            file_name="saop_exceptions.csv",
            mime="text/csv"
        )

with col3:
    if st.button("✓ Submit for Approval", use_container_width=True):
        st.session_state.saop_cycle["forecast_status"] = "Locked"
        st.success("S&OP cycle submitted for executive approval!")

st.divider()

# Risk summary
col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Summary")
    st.markdown(f"""
    **High Risk Items ({len([e for e in exceptions_data if 'Critical' in e['Status'] or 'Action' in e['Status']])}):**
    - Elderflower shortage (€348.5k)
    - Capacity overload (€47.7k exposure)
    - Supplier delays (€156.8k)

    **Mitigation Recommended:**
    1. Expedite Elderflower procurement
    2. Shift non-critical production to Q3
    3. Contact supplier for ETA update
    """)

with col2:
    st.subheader("Cycle Timeline")
    st.markdown("""
    **April 2025 S&OP Cycle:**

    - **2025-04-01** – Cycle opened
    - **2025-04-15** – Demand submitted ✓
    - **2025-04-18** – Supply review in progress
    - **2025-04-21** – Executive review (deadline)
    - **2025-04-25** – Final approval (target)
    - **2025-05-01** – Execution begins
    """)

st.divider()

# Navigation
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📈 View Demand Plan", use_container_width=True):
        st.switch_page("pages/2_Demand.py")

with col2:
    if st.button("📦 View Inventory", use_container_width=True):
        st.switch_page("pages/3_Inventory.py")

with col3:
    if st.button("🔄 Go to Approvals", use_container_width=True):
        st.switch_page("pages/7_Approvals.py")

"""PlanFlow Approvals — Workflow Approvals and Rejections."""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Approvals | PlanFlow", layout="wide")

st.title("Approvals")
st.markdown("Pending approvals and approval history.")

# Sample approval data
approvals_data = [
    {
        "Item": "April 2025 demand plan",
        "Type": "S&OP cycle",
        "Requested By": "Jan Koops",
        "Date": "2025-02-27",
        "Status": "Awaiting exec",
        "Action": "Approve/Reject"
    },
    {
        "Item": "BOLS1GS — safety stock override",
        "Type": "Parameter change",
        "Requested By": "Jan Koops",
        "Date": "2025-02-23",
        "Status": "Pending",
        "Action": "Approve/Reject"
    },
    {
        "Item": "Push to Mono — Apr cycle",
        "Type": "ERP sync",
        "Requested By": "System",
        "Date": "2025-02-28",
        "Status": "Pending",
        "Action": "Approve/Reject"
    },
    {
        "Item": "Promo — Bols Summer campaign",
        "Type": "Promo uplift",
        "Requested By": "Marketing",
        "Date": "2025-02-26",
        "Status": "Pending",
        "Action": "Approve/Reject"
    },
]

approvals_df = pd.DataFrame(approvals_data)

# Count pending
pending_count = len(approvals_df[approvals_df["Status"] != "Approved"])

st.write(f"**{pending_count} items awaiting approval**")

st.divider()

# Display approvals
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.subheader("Pending Approvals")

with col2:
    if st.button("📜 View History", use_container_width=True):
        st.info("Show approved and rejected items")

with col3:
    pass

st.dataframe(
    approvals_df,
    use_container_width=True,
    height=300,
    column_config={
        "Item": st.column_config.TextColumn(width="large"),
        "Type": st.column_config.TextColumn(width="small"),
        "Requested By": st.column_config.TextColumn(width="small"),
        "Date": st.column_config.TextColumn(width="small"),
        "Status": st.column_config.TextColumn(width="small"),
        "Action": st.column_config.TextColumn(width="small"),
    },
    hide_index=True
)

st.divider()

# Quick approval actions
st.subheader("Actions")

col1, col2, col3 = st.columns(3)

with col1:
    selected_approval = st.selectbox(
        "Select item to approve",
        options=[a["Item"] for a in approvals_data],
        key="approval_select"
    )

with col2:
    if st.button("✓ Approve", use_container_width=True):
        st.success(f"✓ Approved: {selected_approval}")
        st.session_state.changes_log.append({
            "timestamp": pd.Timestamp.now(),
            "user": "Jan Koops",
            "module": "Approvals",
            "action": f"Approved {selected_approval}",
            "before": "",
            "after": ""
        })

with col3:
    if st.button("✗ Reject", use_container_width=True):
        st.error(f"✗ Rejected: {selected_approval}")
        st.session_state.changes_log.append({
            "timestamp": pd.Timestamp.now(),
            "user": "Jan Koops",
            "module": "Approvals",
            "action": f"Rejected {selected_approval}",
            "before": "",
            "after": ""
        })

st.divider()

# Approval history
st.subheader("Approval History")

history_data = [
    {
        "Item": "March 2025 demand plan",
        "Type": "S&OP cycle",
        "Date": "2025-02-20",
        "Approved By": "CFO",
        "Status": "Approved ✓"
    },
    {
        "Item": "BOLS1234 — forecast override",
        "Type": "Parameter change",
        "Date": "2025-02-18",
        "Approved By": "Jan Koops",
        "Status": "Approved ✓"
    },
    {
        "Item": "Q1 capacity plan",
        "Type": "Plan",
        "Date": "2025-02-15",
        "Approved By": "Operations",
        "Status": "Approved ✓"
    },
]

history_df = pd.DataFrame(history_data)

st.dataframe(
    history_df,
    use_container_width=True,
    height=200,
    hide_index=True
)

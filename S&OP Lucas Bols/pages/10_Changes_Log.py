"""PlanFlow Changes Log — Full Audit Trail."""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Changes Log | PlanFlow", layout="wide")

st.title("Changes Log")
st.markdown("Complete audit trail of all planning changes and approvals.")

# Sample changes log
changes_data = [
    {
        "Timestamp": "2025-02-28 14:32",
        "User": "Jan Koops",
        "Module": "Demand",
        "Item": "BOL.310204",
        "Change": "Sales forecast Jan 26 updated",
        "Before": "435",
        "After": "490"
    },
    {
        "Timestamp": "2025-02-27 09:15",
        "User": "Jan Koops",
        "Module": "Inventory",
        "Item": "BOL.310200",
        "Change": "Safety stock days updated",
        "Before": "14",
        "After": "28"
    },
    {
        "Timestamp": "2025-02-26 16:45",
        "User": "System",
        "Module": "Connectors",
        "Item": "Vena",
        "Change": "Plan pushed to ERP",
        "Before": "—",
        "After": "—"
    },
    {
        "Timestamp": "2025-02-26 11:22",
        "User": "Marketing",
        "Module": "Promo",
        "Item": "BOL.634714",
        "Change": "Promotion created: +52% uplift",
        "Before": "—",
        "After": "+52%"
    },
    {
        "Timestamp": "2025-02-25 10:05",
        "User": "Jan Koops",
        "Module": "Demand",
        "Item": "All Items",
        "Change": "Final forecast Dec 25 approved",
        "Before": "1,246,365k",
        "After": "1,348,950k"
    },
    {
        "Timestamp": "2025-02-24 15:33",
        "User": "Jan Frost",
        "Module": "Capacity",
        "Item": "Blend Cell",
        "Change": "Capacity utilization overload flag set",
        "Before": "95%",
        "After": "110%"
    },
    {
        "Timestamp": "2025-02-23 08:20",
        "User": "System",
        "Module": "Forecast",
        "Item": "BOL.511200",
        "Change": "Monthly forecast recalculated",
        "Before": "2,450",
        "After": "2,680"
    },
]

changes_df = pd.DataFrame(changes_data)

# Filters
col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_user = st.multiselect(
        "Filter by User",
        options=changes_df["User"].unique().tolist(),
        placeholder="All users"
    )

with col2:
    selected_module = st.multiselect(
        "Filter by Module",
        options=changes_df["Module"].unique().tolist(),
        placeholder="All modules"
    )

with col3:
    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=7), datetime.now()),
        key="changes_date_range"
    )

with col4:
    if st.button("📊 Export", use_container_width=True):
        csv = changes_df.to_csv(index=False)
        st.download_button(
            label="Download Log",
            data=csv,
            file_name="changes_log.csv",
            mime="text/csv"
        )

st.divider()

# Apply filters
filtered_df = changes_df.copy()

if selected_user:
    filtered_df = filtered_df[filtered_df["User"].isin(selected_user)]

if selected_module:
    filtered_df = filtered_df[filtered_df["Module"].isin(selected_module)]

st.subheader(f"Changes ({len(filtered_df)} entries)")

# Display table
st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400,
    column_config={
        "Timestamp": st.column_config.TextColumn(width="small"),
        "User": st.column_config.TextColumn(width="small"),
        "Module": st.column_config.TextColumn(width="small"),
        "Item": st.column_config.TextColumn(width="small"),
        "Change": st.column_config.TextColumn(width="large"),
        "Before": st.column_config.TextColumn(width="small"),
        "After": st.column_config.TextColumn(width="small"),
    },
    hide_index=True
)

st.divider()

# Summary statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Changes", len(changes_df))

with col2:
    st.metric("Users", len(changes_df["User"].unique()))

with col3:
    st.metric("Modules", len(changes_df["Module"].unique()))

with col4:
    st.metric("Items Changed", len(changes_df["Item"].unique()))

st.divider()

# Activity by module
st.subheader("Activity by Module")

module_activity = changes_df.groupby("Module").size().reset_index(name="Count")
module_activity = module_activity.sort_values("Count", ascending=False)

col1, col2 = st.columns([2, 1])

with col1:
    import plotly.express as px

    fig = px.bar(
        module_activity,
        x="Module",
        y="Count",
        title="Changes by Module",
        labels={"Count": "# Changes", "Module": "Module"},
        color="Count",
        color_continuous_scale="Blues"
    )
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Recent Activity:**")
    for _, row in changes_df.head(5).iterrows():
        st.markdown(f"""
        - **{row['Timestamp']}** — {row['User']}
          {row['Module']}: {row['Change']}
        """)

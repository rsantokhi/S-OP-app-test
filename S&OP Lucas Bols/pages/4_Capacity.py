"""PlanFlow Production Capacity Planning — Resource and Workload Management."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import load_item_info, get_monthly_demand
from utils.styling import COLORS

st.set_page_config(page_title="Capacity Planning | PlanFlow", layout="wide")

st.title("Production Capacity Planning")
st.markdown("Monitor manufacturing capacity against demand forecasts.")

# Load data
items = load_item_info()
demand = get_monthly_demand()

# Generate synthetic capacity data
# Create manufacturing groups
manufacturing_groups = {
    "Finished Products Line": {
        "capacity": 17000,
        "current_load": 18754,
    },
    "Intermediate Products Line": {
        "capacity": 12000,
        "current_load": 10500,
    }
}

# Get demand for recent months
recent_demand = demand[demand["year_month"].isin(demand["year_month"].unique()[-12:])].copy()
recent_demand["year_month"] = recent_demand["year_month"].astype(str)

# Create monthly capacity matrix
months = sorted(recent_demand["year_month"].unique())[-8:]  # Last 8 months

capacity_data = []

for group, group_info in manufacturing_groups.items():
    # Get avg demand for this group
    avg_load = group_info["current_load"]

    for i, month in enumerate(months):
        # Add some variation
        monthly_variation = np.sin(i * 0.5) * 0.2
        load = avg_load * (1 + monthly_variation)
        capacity = group_info["capacity"]
        utilization = (load / capacity * 100) if capacity > 0 else 0

        capacity_data.append({
            "Manufacturing Group": group,
            "Month": month,
            "Capacity": int(capacity),
            "Load": int(load),
            "Utilization %": round(utilization, 1),
            "Overhead": 0,
            "Status": "⚠️ Overload" if utilization > 100 else "✓ Normal",
        })

capacity_df = pd.DataFrame(capacity_data)

# Display controls
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.write("")  # Spacer

with col2:
    if st.button("📊 Units"):
        st.session_state.capacity_unit = "units"

with col3:
    if st.button("📥 Export"):
        csv = capacity_df.to_csv(index=False)
        st.download_button(
            label="Download Capacity Plan",
            data=csv,
            file_name="capacity_plan.csv",
            mime="text/csv"
        )

st.divider()

# Capacity matrix table
st.subheader("Capacity Overview by Manufacturing Group")

# Pivot table for better display
pivot_capacity = capacity_df.pivot_table(
    index=["Manufacturing Group"],
    columns="Month",
    values="Capacity",
    aggfunc="first"
)

pivot_load = capacity_df.pivot_table(
    index=["Manufacturing Group"],
    columns="Month",
    values="Load",
    aggfunc="first"
)

pivot_util = capacity_df.pivot_table(
    index=["Manufacturing Group"],
    columns="Month",
    values="Utilization %",
    aggfunc="first"
)

# Display in expandable sections
for group in manufacturing_groups.keys():
    with st.expander(f"📦 {group}", expanded=True):
        group_data = capacity_df[capacity_df["Manufacturing Group"] == group].copy()

        col1, col2, col3 = st.columns(3)

        with col1:
            avg_capacity = group_data["Capacity"].iloc[0]
            st.metric("Total Capacity", f"{int(avg_capacity):,} units/month")

        with col2:
            avg_load = group_data["Load"].mean()
            st.metric("Avg Load", f"{int(avg_load):,} units/month")

        with col3:
            avg_util = group_data["Utilization %"].mean()
            color = "🔴" if avg_util > 100 else "🟢"
            st.metric(f"{color} Avg Utilization", f"{avg_util:.1f}%")

        # Mini table
        table_display = group_data[[
            "Month",
            "Capacity",
            "Load",
            "Utilization %",
            "Status"
        ]].copy()

        table_display["Capacity"] = table_display["Capacity"].astype(int)
        table_display["Load"] = table_display["Load"].astype(int)

        # Highlight overloaded rows
        def highlight_overload(row):
            if row["Utilization %"] > 100:
                return ["background-color: rgba(204, 34, 0, 0.15)"] * len(row)
            return [""] * len(row)

        st.dataframe(
            table_display,
            use_container_width=True,
            height=250,
            column_config={
                col: st.column_config.NumberColumn(format="%d") for col in ["Capacity", "Load", "Utilization %"]
            }
        )

st.divider()

# Capacity chart
st.subheader("Capacity vs Load Trend")

col1, col2 = st.columns(2)

for idx, group in enumerate(manufacturing_groups.keys()):
    with col1 if idx == 0 else col2:
        group_data = capacity_df[capacity_df["Manufacturing Group"] == group].copy()

        fig = go.Figure()

        # Add capacity line
        fig.add_trace(go.Bar(
            x=group_data["Month"],
            y=group_data["Capacity"],
            name="Capacity",
            marker_color=COLORS["success_green"],
            opacity=0.6,
        ))

        # Add load line
        fig.add_trace(go.Bar(
            x=group_data["Month"],
            y=group_data["Load"],
            name="Load",
            marker_color=COLORS["accent_orange"],
            opacity=0.7,
        ))

        # Add 100% line
        fig.add_hline(
            y=manufacturing_groups[group]["capacity"],
            annotation_text="100% Utilization",
            annotation_position="right",
            line_dash="dash",
            line_color=COLORS["danger_red"]
        )

        fig.update_layout(
            title=f"{group}",
            xaxis_title="Month",
            yaxis_title="Units",
            barmode="group",
            hovermode="x unified",
            height=350,
            font=dict(size=10),
            plot_bgcolor="rgba(245,245,242,0.5)",
        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()

# Bottleneck analysis
st.subheader("Bottleneck Analysis")

overloaded = capacity_df[capacity_df["Utilization %"] > 100]

if len(overloaded) > 0:
    st.warning(f"⚠️ {len(overloaded)} capacity violations detected")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Overloaded Periods:**")
        for _, row in overloaded.iterrows():
            st.markdown(f"""
            - **{row['Manufacturing Group']}** — {row['Month']}
              - Utilization: {row['Utilization %']:.1f}% (capacity: {int(row['Capacity']):,} units)
            """)

    with col2:
        st.markdown("**Recommended Actions:**")
        st.markdown("""
        1. **Increase shift hours** — Add overtime on production lines
        2. **Outsource production** — Sub-contract excess demand
        3. **Defer demand** — Adjust forecast or request delivery delays
        4. **Invest in capacity** — Add equipment (capital expenditure)
        5. **Optimize scheduling** — Shift non-critical items to available capacity
        """)

else:
    st.success("✓ All manufacturing groups have sufficient capacity.")

st.divider()

# Capacity settings
col1, col2 = st.columns(2)

with col1:
    if st.button("⚙️ Configure Capacity", use_container_width=True):
        st.info("Capacity settings can be configured in the Settings page.")

with col2:
    if st.button("📊 View Demand Plan", use_container_width=True):
        st.switch_page("pages/2_Demand.py")

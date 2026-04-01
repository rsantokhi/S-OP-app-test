"""PlanFlow Promo Planning — Promotion Calendar and Uplift Management."""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Promo Planning | PlanFlow", layout="wide")

st.title("Promo Planning")
st.markdown("Manage promotional campaigns and demand uplift planning.")

# Sample promotions data
promos_data = [
    {
        "Promotion": "Summer Galliano campaign",
        "SKU/Category": "Galliano range",
        "Channel": "Retail NL",
        "Start": "2025-06-20",
        "End": "2025-08-20",
        "Uplift %": "+32%",
        "Uplift Units": "€9,000",
        "Status": "Approved ✓"
    },
    {
        "Promotion": "Bols Summer push — DDC",
        "SKU/Category": "Bols Liqueur",
        "Channel": "DDC / Online",
        "Start": "2025-06-10",
        "End": "2025-06-20",
        "Uplift %": "+18%",
        "Uplift Units": "€1,000",
        "Status": "Pending ⏳"
    },
    {
        "Promotion": "Elderflower limited edition",
        "SKU/Category": "BOL511200",
        "Channel": "All channels",
        "Start": "2025-04-20",
        "End": "2025-06-20",
        "Uplift %": "+85%",
        "Uplift Units": "€3,600",
        "Status": "Draft"
    },
    {
        "Promotion": "Year-end Cocktails promo",
        "SKU/Category": "Cocktails",
        "Channel": "Retail EU",
        "Start": "2025-12-22",
        "End": "2026-01-26",
        "Uplift %": "+20%",
        "Uplift Units": "€2,100",
        "Status": "Draft"
    },
]

promos_df = pd.DataFrame(promos_data)

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.write("")

with col2:
    if st.button("📅 Import Calendar", use_container_width=True):
        st.info("Import promotional calendar from external source")

with col3:
    if st.button("+ New Promotion", use_container_width=True):
        st.info("Create new promotional campaign")

st.divider()

# Display promotions
st.subheader("Promotional Calendar")

st.dataframe(
    promos_df,
    use_container_width=True,
    height=300,
    column_config={
        "Promotion": st.column_config.TextColumn(width="large"),
        "SKU/Category": st.column_config.TextColumn(width="small"),
        "Channel": st.column_config.TextColumn(width="small"),
        "Start": st.column_config.TextColumn(width="small"),
        "End": st.column_config.TextColumn(width="small"),
        "Uplift %": st.column_config.TextColumn(width="small"),
        "Uplift Units": st.column_config.TextColumn(width="small"),
        "Status": st.column_config.TextColumn(width="small"),
    },
    hide_index=True
)

st.divider()

# Promo impact analysis
st.subheader("Impact on Demand Forecast")

col1, col2 = st.columns(2)

with col1:
    selected_promo = st.selectbox(
        "Select promotion to view impact",
        options=[p["Promotion"] for p in promos_data],
    )

with col2:
    st.write("")  # Spacer

if selected_promo:
    promo_info = next((p for p in promos_data if p["Promotion"] == selected_promo), None)

    if promo_info:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Uplift %", promo_info["Uplift %"])

        with col2:
            st.metric("Uplift Units", promo_info["Uplift Units"])

        with col3:
            st.metric("Duration", f"{promo_info['Start']} to {promo_info['End']}")

        st.info(f"""
        **Promotion:** {promo_info['Promotion']}
        **Category:** {promo_info['SKU/Category']}
        **Channel:** {promo_info['Channel']}
        **Status:** {promo_info['Status']}

        Impact on demand forecast has been calculated and incorporated into demand planning.
        """)

st.divider()

# Create/Edit promotion form
st.subheader("Promotion Details")

with st.expander("Edit Selected Promotion", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        promo_name = st.text_input("Promotion Name", value=selected_promo if selected_promo else "")
        skus = st.text_input("SKUs/Categories", placeholder="e.g., BOLS1234, Bols Liqueur")
        channel = st.selectbox("Channel", ["Retail NL", "DDC", "Online", "All channels", "Retail EU"])

    with col2:
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        uplift_pct = st.number_input("Uplift %", min_value=0, max_value=500, value=20, step=5)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✓ Save", use_container_width=True):
            st.success("✓ Promotion saved!")

    with col2:
        if st.button("📊 Preview Impact", use_container_width=True):
            st.info("Demand impact preview would display here")

    with col3:
        if st.button("🗑️ Delete", use_container_width=True):
            st.warning("Promotion deleted")

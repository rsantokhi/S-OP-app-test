"""PlanFlow New Products — NPI Tracking and Launch Planning."""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="New Products | PlanFlow", layout="wide")

st.title("New Products (NPI)")
st.markdown("Track new product introductions and launch planning.")

# Sample NPI data
npi_data = [
    {
        "Product": "Bols Coconut 70cNL",
        "Category": "Bols Liqueur",
        "Launch Date": "2025-07-15",
        "Comparable SKU": "BOL.320384",
        "Initial Forecast": "1,180 /mo",
        "Channel": "Retail NL",
        "Status": "Active ✓"
    },
    {
        "Product": "Galliano Espresso EU 0.7L",
        "Category": "Galliano",
        "Launch Date": "2025-09-01",
        "Comparable SKU": "BOL.540713.1",
        "Initial Forecast": "850 /mo",
        "Channel": "DDC - Retail",
        "Status": "In planning ⏳"
    },
    {
        "Product": "Bols RTD Elderflower Spritz",
        "Category": "RTD",
        "Launch Date": "2026-01-15",
        "Comparable SKU": "BOL.610201",
        "Initial Forecast": "2,480 /mo",
        "Channel": "All channels",
        "Status": "Draft"
    },
]

npi_df = pd.DataFrame(npi_data)

# Action buttons
col1, col2 = st.columns([3, 1])

with col1:
    st.write("")

with col2:
    if st.button("+ Add New Product", use_container_width=True):
        st.info("Create new product introduction")

st.divider()

# Display NPI
st.subheader("New Product Pipeline")

st.dataframe(
    npi_df,
    use_container_width=True,
    height=300,
    column_config={
        "Product": st.column_config.TextColumn(width="large"),
        "Category": st.column_config.TextColumn(width="small"),
        "Launch Date": st.column_config.TextColumn(width="small"),
        "Comparable SKU": st.column_config.TextColumn(width="small"),
        "Initial Forecast": st.column_config.TextColumn(width="small"),
        "Channel": st.column_config.TextColumn(width="small"),
        "Status": st.column_config.TextColumn(width="small"),
    },
    hide_index=True
)

st.divider()

# NPI details
st.subheader("Product Launch Planning")

selected_product = st.selectbox(
    "Select product to view/edit",
    options=[n["Product"] for n in npi_data],
)

if selected_product:
    npi_info = next((n for n in npi_data if n["Product"] == selected_product), None)

    if npi_info:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Product Info")
            st.markdown(f"""
            **Product:** {npi_info['Product']}
            **Category:** {npi_info['Category']}
            **Status:** {npi_info['Status']}
            """)

            st.divider()

            st.markdown("**Launch Plan:**")
            st.markdown(f"""
            - **Launch Date:** {npi_info['Launch Date']}
            - **Channel:** {npi_info['Channel']}
            - **Comparable Product:** {npi_info['Comparable SKU']}
            """)

        with col2:
            st.subheader("Forecast")
            st.metric("Initial Monthly Forecast", npi_info["Initial Forecast"])

            st.divider()

            st.markdown("**Forecast Methodology:**")
            st.markdown("""
            - Based on comparable product: {0}
            - Adjusted for market conditions and channel
            - Confidence level: Medium
            """.format(npi_info["Comparable SKU"]))

        st.divider()

        # Edit form
        with st.expander("Edit Product Details", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                product_name = st.text_input("Product Name", value=npi_info["Product"])
                category = st.text_input("Category", value=npi_info["Category"])
                launch_date = st.date_input("Launch Date", value=pd.to_datetime(npi_info["Launch Date"]))

            with col2:
                comparable = st.text_input("Comparable SKU", value=npi_info["Comparable SKU"])
                forecast = st.number_input("Initial Monthly Forecast (units)", min_value=0, value=1000, step=100)
                channel = st.selectbox("Channel", ["Retail NL", "DDC", "Online", "All channels"], key="npi_channel")

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("✓ Save", use_container_width=True):
                    st.success("✓ Product updated!")

            with col2:
                if st.button("📊 View Forecast Impact", use_container_width=True):
                    st.info("Forecast impact would display here")

            with col3:
                if st.button("🗑️ Delete", use_container_width=True):
                    st.warning("Product removed from NPI pipeline")

st.divider()

# NPI status summary
col1, col2, col3 = st.columns(3)

with col1:
    active_count = len([n for n in npi_data if "Active" in n["Status"]])
    st.metric("Active Products", active_count)

with col2:
    planning_count = len([n for n in npi_data if "planning" in n["Status"].lower()])
    st.metric("In Planning", planning_count)

with col3:
    draft_count = len([n for n in npi_data if "Draft" in n["Status"]])
    st.metric("Draft", draft_count)

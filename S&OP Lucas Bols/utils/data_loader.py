"""Data loading functions for PlanFlow from Excel."""

import pandas as pd
import streamlit as st
from pathlib import Path


# Get the data file path (assumes it's in the same directory as app.py)
DATA_FILE = Path(__file__).parent.parent / "LB_Transactional_Data.xlsx"


@st.cache_data
def load_transactions() -> pd.DataFrame:
    """Load transaction history from Excel."""
    df = pd.read_excel(DATA_FILE, sheet_name="Transactions")
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Parse date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

    # Add year/month columns for grouping
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["year_month"] = df["date"].dt.to_period("M")

    return df


@st.cache_data
def load_item_info() -> pd.DataFrame:
    """Load item master data from Excel."""
    df = pd.read_excel(DATA_FILE, sheet_name="Item info")
    df.columns = df.columns.str.strip().str.lower()

    # Standardize key columns
    if "item code" in df.columns:
        df = df.rename(columns={"item code": "item_code"})
    if "item description" in df.columns:
        df = df.rename(columns={"item description": "description"})
    if "item category" in df.columns:
        df = df.rename(columns={"item category": "category"})
    if "last on hand" in df.columns:
        df = df.rename(columns={"last on hand": "on_hand"})
    if "inventory value/unit" in df.columns:
        df = df.rename(columns={"inventory value/unit": "unit_value"})
    if "lead time" in df.columns:
        df = df.rename(columns={"lead time": "lead_time_days"})
    if "min lot" in df.columns:
        df = df.rename(columns={"min lot": "min_order_qty"})
    if "supplier code" in df.columns:
        df = df.rename(columns={"supplier code": "supplier"})
    if "dc name (multi-echelon)" in df.columns:
        df = df.rename(columns={"dc name (multi-echelon)": "distribution_center"})

    # Ensure numeric columns
    numeric_cols = ["on_hand", "unit_value", "lead_time_days", "min_order_qty"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


@st.cache_data
def load_orders_in() -> pd.DataFrame:
    """Load incoming purchase orders."""
    df = pd.read_excel(DATA_FILE, sheet_name="Orders to receive")
    df.columns = df.columns.str.strip().str.lower()

    # Standardize columns
    if "item code" in df.columns:
        df = df.rename(columns={"item code": "item_code"})
    if "qty to receive" in df.columns:
        df = df.rename(columns={"qty to receive": "quantity"})
    if "delivery date" in df.columns:
        df["delivery_date"] = pd.to_datetime(df["delivery date"], errors="coerce")
    if "sendout date" in df.columns:
        df["sendout_date"] = pd.to_datetime(df["sendout date"], errors="coerce")

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    return df


@st.cache_data
def load_orders_out() -> pd.DataFrame:
    """Load outgoing shipment orders."""
    df = pd.read_excel(DATA_FILE, sheet_name="Orders to ship")
    df.columns = df.columns.str.strip().str.lower()

    # Standardize columns
    if "item code" in df.columns:
        df = df.rename(columns={"item code": "item_code"})
    if "qty to ship" in df.columns:
        df = df.rename(columns={"qty to ship": "quantity"})
    if "shipment date" in df.columns:
        df["shipment_date"] = pd.to_datetime(df["shipment date"], errors="coerce")

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    return df


@st.cache_data
def load_bom() -> pd.DataFrame:
    """Load bill of materials."""
    df = pd.read_excel(DATA_FILE, sheet_name="Bill of materials")
    df.columns = df.columns.str.strip().str.lower()

    # Standardize columns
    if "finished good's code" in df.columns:
        df = df.rename(columns={"finished good's code": "finished_good_code"})
    if "material's code" in df.columns:
        df = df.rename(columns={"material's code": "material_code"})
    if "material qty/batch" in df.columns:
        df = df.rename(columns={"material qty/batch": "material_qty"})
    if "batch rounding" in df.columns:
        df = df.rename(columns={"batch rounding": "batch_rounding"})

    df["material_qty"] = pd.to_numeric(df["material_qty"], errors="coerce")
    df["batch_rounding"] = pd.to_numeric(df["batch_rounding"], errors="coerce")
    return df


@st.cache_data
def get_monthly_demand() -> pd.DataFrame:
    """
    Aggregate transactions into monthly demand by item code.

    Returns:
        DataFrame with columns: item_code, year_month, quantity, revenue
    """
    transactions = load_transactions()

    demand = transactions.groupby(["item_code", "year_month"]).agg({
        "quantity sold": "sum",
        "transaction revenue": "sum"
    }).reset_index()

    demand.columns = ["item_code", "year_month", "quantity", "revenue"]
    return demand


@st.cache_data
def get_demand_by_item_and_month() -> dict:
    """
    Get demand as a nested dict for easy access: {item_code: {year_month: quantity}}

    Returns:
        Dictionary structure
    """
    demand = get_monthly_demand()
    result = {}
    for _, row in demand.iterrows():
        item = row["item_code"]
        period = row["year_month"]
        qty = row["quantity"]

        if item not in result:
            result[item] = {}
        result[item][period] = qty

    return result


def get_unique_items() -> list:
    """Get list of unique item codes."""
    items = load_item_info()
    return sorted(items["item_code"].dropna().unique().tolist())


def get_item_by_code(item_code: str) -> dict:
    """Get item info as dictionary."""
    items = load_item_info()
    row = items[items["item_code"] == item_code]

    if row.empty:
        return None

    return row.iloc[0].to_dict()


def get_item_categories() -> list:
    """Get unique item categories."""
    items = load_item_info()
    return sorted(items["category"].dropna().unique().tolist())


def get_items_by_category(category: str) -> list:
    """Get item codes for a specific category."""
    items = load_item_info()
    return sorted(items[items["category"] == category]["item_code"].unique().tolist())


def get_incoming_quantity(item_code: str, period=None) -> float:
    """
    Get total quantity expected to arrive for an item.

    Args:
        item_code: Item code
        period: Optional period to filter by (pandas Period)

    Returns:
        Total incoming quantity
    """
    orders_in = load_orders_in()
    orders = orders_in[orders_in["item_code"] == item_code]

    if period:
        orders = orders[orders["delivery_date"].dt.to_period("M") == period]

    return orders["quantity"].sum() if not orders.empty else 0


def get_outgoing_quantity(item_code: str, period=None) -> float:
    """
    Get total quantity expected to ship for an item.

    Args:
        item_code: Item code
        period: Optional period to filter by (pandas Period)

    Returns:
        Total outgoing quantity
    """
    orders_out = load_orders_out()
    orders = orders_out[orders_out["item_code"] == item_code]

    if period:
        orders = orders[orders["shipment_date"].dt.to_period("M") == period]

    return orders["quantity"].sum() if not orders.empty else 0


def calculate_days_on_hand(item_code: str, avg_daily_demand: float) -> float:
    """
    Calculate days of inventory on hand.

    Args:
        item_code: Item code
        avg_daily_demand: Average daily demand quantity

    Returns:
        Days on hand (float)
    """
    if avg_daily_demand <= 0:
        return 0

    item = get_item_by_code(item_code)
    if not item or pd.isna(item.get("on_hand")):
        return 0

    on_hand = item["on_hand"]
    return on_hand / avg_daily_demand


def get_last_sync_date() -> str:
    """Get last sync date from items (if available)."""
    items = load_item_info()
    # Assuming there might be a last_sync column (not in current data, but common)
    # For now, return "not synced" or current time
    return "Not available"

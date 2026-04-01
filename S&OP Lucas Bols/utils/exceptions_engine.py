"""Exception detection engine for supply chain planning."""

import pandas as pd
import numpy as np


def detect_shortage(items_df: pd.DataFrame, orders_in_df: pd.DataFrame, demand_monthly_avg: dict) -> list:
    """
    Detect shortage exceptions.

    Rule: (on_hand + orders_in) / avg_monthly_demand < lead_time_months

    Args:
        items_df: Item master dataframe
        orders_in_df: Incoming orders dataframe
        demand_monthly_avg: Dict mapping item_code to avg monthly demand

    Returns:
        List of shortage exceptions
    """
    exceptions = []

    for _, item in items_df.iterrows():
        item_code = item["item_code"]
        on_hand = item.get("on_hand", 0)
        lead_time_days = item.get("lead_time_days", 30)
        lead_time_months = lead_time_days / 30.0

        # Get incoming quantity
        incoming = orders_in_df[orders_in_df["item_code"] == item_code]["quantity"].sum()

        # Get avg monthly demand
        avg_demand = demand_monthly_avg.get(item_code, 0)

        if avg_demand > 0:
            available_months = (on_hand + incoming) / avg_demand

            if available_months < lead_time_months:
                exceptions.append({
                    "type": "Shortage",
                    "item_code": item_code,
                    "description": f"{item.get('description', item_code)} — stockout risk in {available_months:.1f} months",
                    "severity": "HIGH" if available_months < lead_time_months / 2 else "MEDIUM",
                    "available_supply_months": available_months,
                    "lead_time_months": lead_time_months,
                })

    return exceptions


def detect_overstock(items_df: pd.DataFrame, demand_monthly_avg: dict, threshold_doh: int = 190) -> list:
    """
    Detect overstock exceptions.

    Rule: days_on_hand > threshold_doh

    Args:
        items_df: Item master dataframe
        demand_monthly_avg: Dict mapping item_code to avg monthly demand
        threshold_doh: Threshold for days on hand (default 190)

    Returns:
        List of overstock exceptions
    """
    exceptions = []

    for _, item in items_df.iterrows():
        item_code = item["item_code"]
        on_hand = item.get("on_hand", 0)
        avg_demand = demand_monthly_avg.get(item_code, 1)

        if avg_demand > 0:
            doh = (on_hand / (avg_demand / 30.0))

            if doh > threshold_doh:
                exceptions.append({
                    "type": "Overstock",
                    "item_code": item_code,
                    "description": f"{item.get('description', item_code)} — {int(doh)} days on hand",
                    "severity": "MEDIUM" if doh < threshold_doh * 1.5 else "HIGH",
                    "days_on_hand": doh,
                    "threshold_doh": threshold_doh,
                })

    return exceptions


def detect_capacity_breach(capacity_data: dict, utilization_threshold: float = 100.0) -> list:
    """
    Detect capacity planning exceptions.

    Rule: utilisation > utilization_threshold

    Args:
        capacity_data: Dict with manufacturing group data
        utilization_threshold: Threshold % for utilization (default 100%)

    Returns:
        List of capacity exceptions
    """
    exceptions = []

    for group_name, group_info in capacity_data.items():
        capacity = group_info.get("capacity", 1)
        load = group_info.get("load", 0)
        month = group_info.get("month", "")

        utilization = (load / capacity * 100) if capacity > 0 else 0

        if utilization > utilization_threshold:
            exceptions.append({
                "type": "Capacity Breach",
                "group": group_name,
                "month": month,
                "description": f"{group_name} — {utilization:.1f}% utilization in {month}",
                "severity": "HIGH" if utilization > utilization_threshold * 1.2 else "MEDIUM",
                "capacity": capacity,
                "load": load,
                "utilization_pct": utilization,
            })

    return exceptions


def detect_forecast_accuracy_issue(items_df: pd.DataFrame, mape_threshold: float = 20.0) -> list:
    """
    Detect forecast accuracy exceptions.

    Rule: MAPE > mape_threshold for recent period

    Args:
        items_df: Item master with forecast accuracy metrics (if available)
        mape_threshold: Threshold % for MAPE (default 20%)

    Returns:
        List of forecast accuracy exceptions
    """
    exceptions = []

    # This is a placeholder — would require forecast accuracy metrics in items_df
    # For now, return empty list

    return exceptions


def detect_supplier_issues(orders_in_df: pd.DataFrame, lead_time_dict: dict, days_delay_threshold: int = 7) -> list:
    """
    Detect supplier and supply chain exceptions.

    Rule: Delivery date is past due or within warning period

    Args:
        orders_in_df: Incoming orders dataframe
        lead_time_dict: Dict mapping item_code to lead time days
        days_delay_threshold: Days threshold for flagging (default 7)

    Returns:
        List of supplier exceptions
    """
    from datetime import datetime, timedelta

    exceptions = []

    today = pd.Timestamp.now()

    for _, order in orders_in_df.iterrows():
        delivery_date = pd.to_datetime(order.get("delivery_date"), errors="coerce")

        if pd.isna(delivery_date):
            continue

        days_until_delivery = (delivery_date - today).days

        if days_until_delivery < 0:
            exceptions.append({
                "type": "Supply Delay",
                "item_code": order["item_code"],
                "supplier": order.get("supplier", "Unknown"),
                "description": f"Order delayed {abs(days_until_delivery)} days (delivery: {delivery_date.date()})",
                "severity": "HIGH",
                "overdue_days": abs(days_until_delivery),
            })

        elif days_until_delivery < days_delay_threshold:
            exceptions.append({
                "type": "Supply at Risk",
                "item_code": order["item_code"],
                "supplier": order.get("supplier", "Unknown"),
                "description": f"Order arriving in {days_until_delivery} days (delivery: {delivery_date.date()})",
                "severity": "MEDIUM",
                "days_remaining": days_until_delivery,
            })

    return exceptions


def run_exception_detection(items_df: pd.DataFrame, orders_in_df: pd.DataFrame, demand_monthly_avg: dict,
                           capacity_data: dict = None) -> list:
    """
    Run full exception detection across all rules.

    Args:
        items_df: Item master dataframe
        orders_in_df: Incoming orders dataframe
        demand_monthly_avg: Dict mapping item_code to avg monthly demand
        capacity_data: Optional capacity data dictionary

    Returns:
        Combined list of all exceptions
    """
    all_exceptions = []

    # Run all detectors
    all_exceptions.extend(detect_shortage(items_df, orders_in_df, demand_monthly_avg))
    all_exceptions.extend(detect_overstock(items_df, demand_monthly_avg))
    all_exceptions.extend(detect_supplier_issues(orders_in_df, {}))

    if capacity_data:
        all_exceptions.extend(detect_capacity_breach(capacity_data))

    # Sort by severity
    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    all_exceptions.sort(key=lambda x: severity_order.get(x.get("severity", "LOW"), 3))

    return all_exceptions


def get_exception_impact_estimate(exception: dict) -> float:
    """
    Estimate financial impact of an exception.

    Args:
        exception: Exception dictionary

    Returns:
        Estimated impact in EUR (positive = loss, negative = gain)
    """
    exception_type = exception.get("type")

    if exception_type == "Shortage":
        # Estimate lost revenue
        return 10000 * exception.get("severity" == "HIGH" and 3 or 1)

    elif exception_type == "Overstock":
        # Estimate carrying cost and depreciation
        doh = exception.get("days_on_hand", 100)
        return 500 * (doh / 30)  # ~€500/month per item in overstock

    elif exception_type == "Capacity Breach":
        # Estimate cost of overtime or outsourcing
        excess_util = exception.get("utilization_pct", 100) - 100
        return 2000 * (excess_util / 10)

    elif exception_type == "Supply Delay":
        # Estimate rush freight or expedite cost
        return 1000 + (500 * exception.get("overdue_days", 1))

    else:
        return 0

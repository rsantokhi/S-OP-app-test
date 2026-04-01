"""PlanFlow styling and theme utilities."""

import streamlit as st

# PlanFlow color palette
COLORS = {
    "primary_blue": "#0066CC",
    "accent_orange": "#E8720C",
    "success_green": "#007744",
    "warning_amber": "#885500",
    "danger_red": "#CC2200",
    "bg_light": "#F5F5F2",
    "bg_white": "#FFFFFF",
    "text_primary": "#0066CC",
    "text_secondary": "#4a6080",
    "text_tertiary": "#8898aa",
    "border": "#e0e8f0",
}


def inject_css():
    """Inject custom PlanFlow CSS theme into Streamlit app."""
    css = f"""
    <style>
    :root {{
        --blue: {COLORS['primary_blue']};
        --orange: {COLORS['accent_orange']};
        --green: {COLORS['success_green']};
        --amber: {COLORS['warning_amber']};
        --red: {COLORS['danger_red']};
        --bg-light: {COLORS['bg_light']};
        --bg-white: {COLORS['bg_white']};
    }}

    /* Main background */
    body {{
        background-color: {COLORS['bg_light']};
    }}

    /* Sidebar */
    .stSidebar {{
        background-color: {COLORS['bg_white']};
    }}

    /* Navigation sections */
    .nav-section {{
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: {COLORS['text_tertiary']};
        margin-top: 20px;
        margin-bottom: 8px;
        padding: 0 10px;
    }}

    /* Active nav item */
    .stNavLink [data-testid="stMarkdownContainer"] p {{
        margin: 0;
    }}

    /* Badges / Pills */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 9px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
        margin-left: 6px;
    }}

    .badge-green {{
        background-color: rgba(0, 119, 68, 0.1);
        color: {COLORS['success_green']};
        border: 1px solid rgba(0, 119, 68, 0.3);
    }}

    .badge-orange {{
        background-color: rgba(232, 114, 12, 0.1);
        color: {COLORS['accent_orange']};
        border: 1px solid rgba(232, 114, 12, 0.3);
    }}

    .badge-red {{
        background-color: rgba(204, 34, 0, 0.1);
        color: {COLORS['danger_red']};
        border: 1px solid rgba(204, 34, 0, 0.3);
    }}

    .badge-blue {{
        background-color: rgba(0, 102, 204, 0.1);
        color: {COLORS['primary_blue']};
        border: 1px solid rgba(0, 102, 204, 0.3);
    }}

    .badge-grey {{
        background-color: rgba(128, 128, 128, 0.1);
        color: #666;
        border: 1px solid rgba(128, 128, 128, 0.3);
    }}

    /* Status badges */
    .status-submitted {{
        background-color: rgba(0, 119, 68, 0.15);
        color: {COLORS['success_green']};
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
    }}

    .status-draft {{
        background-color: rgba(232, 114, 12, 0.15);
        color: {COLORS['accent_orange']};
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
    }}

    .status-pending {{
        background-color: rgba(232, 114, 12, 0.15);
        color: {COLORS['accent_orange']};
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
    }}

    .status-approved {{
        background-color: rgba(0, 119, 68, 0.15);
        color: {COLORS['success_green']};
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
    }}

    /* Metric cards */
    .metric-card {{
        background: {COLORS['bg_white']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }}

    .metric-label {{
        font-size: 12px;
        color: {COLORS['text_tertiary']};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}

    .metric-value {{
        font-size: 28px;
        font-weight: 700;
        color: {COLORS['primary_blue']};
        margin: 8px 0;
    }}

    .metric-delta {{
        font-size: 12px;
        color: {COLORS['text_secondary']};
    }}

    .metric-delta.positive {{
        color: {COLORS['success_green']};
    }}

    .metric-delta.negative {{
        color: {COLORS['danger_red']};
    }}

    /* Row highlighting */
    .row-alert {{
        background-color: rgba(232, 114, 12, 0.1) !important;
    }}

    .row-success {{
        background-color: rgba(0, 119, 68, 0.1) !important;
    }}

    .row-danger {{
        background-color: rgba(204, 34, 0, 0.1) !important;
    }}

    /* Table styling */
    .stDataFrame {{
        font-size: 13px;
    }}

    thead {{
        background-color: {COLORS['bg_light']} !important;
    }}

    /* Sidebar footer */
    .sidebar-footer {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        right: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        padding-top: 12px;
        border-top: 1px solid {COLORS['border']};
    }}

    .user-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: {COLORS['primary_blue']};
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 600;
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def badge(text: str, color: str = "blue", count: int = None) -> str:
    """
    Create a colored badge/pill.

    Args:
        text: Badge text
        color: One of ['green', 'orange', 'red', 'blue', 'grey']
        count: Optional count to display in badge

    Returns:
        HTML string for badge
    """
    count_str = f" <strong>{count}</strong>" if count else ""
    return f'<span class="badge badge-{color}">{text}{count_str}</span>'


def metric_card(label: str, value: str, delta: str = None, delta_positive: bool = None) -> str:
    """
    Create a metric card with label, value, and optional delta.

    Args:
        label: Card label (e.g. "Total Inventory Value")
        value: Main metric value (e.g. "€88.5M")
        delta: Optional delta text (e.g. "-€4.2M vs last month")
        delta_positive: If True, delta is green; if False, red; if None, grey

    Returns:
        HTML string for metric card
    """
    delta_class = ""
    if delta:
        if delta_positive is True:
            delta_class = "positive"
        elif delta_positive is False:
            delta_class = "negative"

    delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>' if delta else ""

    html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    return html


def status_badge(status: str) -> str:
    """
    Create a status badge.

    Args:
        status: One of ['draft', 'pending', 'submitted', 'approved', 'rejected']

    Returns:
        HTML string for status badge
    """
    status_lower = status.lower()
    return f'<span class="status-{status_lower}">{status}</span>'


def highlight_row_color(val: float, threshold_high: float = 100, threshold_low: float = 50) -> str:
    """
    Return CSS to highlight table cells based on value.
    Used with pandas Styler.applymap()

    Args:
        val: Numeric value
        threshold_high: Values above this get red background
        threshold_low: Values below this get yellow background

    Returns:
        CSS string for cell styling
    """
    if val is None or isinstance(val, str):
        return ""

    try:
        val = float(val)
    except (ValueError, TypeError):
        return ""

    if val > threshold_high:
        return "background-color: #fff0ee; color: #cc2200"  # Red
    elif val < threshold_low:
        return "background-color: #fffbee; color: #885500"  # Amber
    else:
        return ""

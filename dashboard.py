"""
Blinkit Sales Performance Dashboard (Streamlit)

Run: streamlit run dashboard.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st

HERE = Path(__file__).parent
DATA_PATH = HERE / "data" / "BlinkIT Grocery Data.csv"

# ---------------------------------------------------------------------------
# Blinkit brand palette
# ---------------------------------------------------------------------------
YELLOW = "#F8CB45"
YELLOW_DARK = "#E0AC00"
YELLOW_LIGHT = "#FFF0C2"
GREEN = "#54B226"
BLACK = "#1F1F1F"
GRAY = "#6B6B6B"
WHITE = "#FFFFFF"

BRAND_SEQUENCE = [YELLOW, BLACK, GREEN, "#F4A300", "#8BC34A", "#4D4D4D", "#FFE082", "#2E7D32"]

st.set_page_config(page_title="Blinkit Sales Dashboard", page_icon="⚡", layout="wide")

# ---------------------------------------------------------------------------
# Theme: Blinkit-style CSS (yellow/black, rounded sans-serif font)
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif !important;
    }}

    .stApp {{
        background-color: {WHITE};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {BLACK};
    }}
    section[data-testid="stSidebar"] * {{
        color: {WHITE} !important;
        font-family: 'Poppins', sans-serif !important;
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {YELLOW} !important;
        font-weight: 700 !important;
    }}
    span[data-baseweb="tag"] {{
        background-color: {YELLOW} !important;
        color: {BLACK} !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }}
    span[data-baseweb="tag"] svg {{
        fill: {BLACK} !important;
    }}
    section[data-testid="stSidebar"] .blinkit-badge {{
        color: {BLACK} !important;
    }}
    section[data-testid="stSidebar"] .blinkit-badge span {{
        color: {GREEN} !important;
    }}

    .blinkit-header {{
        display: flex;
        align-items: center;
        gap: 16px;
        background: {BLACK};
        padding: 18px 28px;
        border-radius: 16px;
        margin-bottom: 22px;
    }}
    .blinkit-badge {{
        background: {YELLOW};
        color: {BLACK};
        font-weight: 800;
        font-size: 26px;
        letter-spacing: -0.5px;
        padding: 6px 16px;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
    }}
    .blinkit-badge span {{
        color: {GREEN};
    }}
    .blinkit-tagline {{
        color: {WHITE};
        font-size: 15px;
        font-weight: 500;
        opacity: 0.85;
    }}
    .blinkit-title {{
        color: {WHITE};
        font-size: 22px;
        font-weight: 700;
        margin: 0;
    }}

    div[data-testid="stMetric"] {{
        background: {WHITE};
        border: 2px solid {YELLOW};
        border-left: 8px solid {YELLOW};
        border-radius: 14px;
        padding: 14px 18px 10px 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    div[data-testid="stMetric"] label {{
        color: {GRAY} !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: {BLACK} !important;
        font-weight: 800 !important;
    }}

    h1, h2, h3, h4 {{
        color: {BLACK} !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
    }}

    .stButton>button, .stDownloadButton>button {{
        background-color: {YELLOW};
        color: {BLACK};
        font-weight: 700;
        border-radius: 10px;
        border: none;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Plotly theme to match the brand palette
pio.templates["blinkit"] = pio.templates["plotly_white"]
pio.templates["blinkit"].layout.colorway = BRAND_SEQUENCE
pio.templates["blinkit"].layout.font = dict(family="Poppins, sans-serif", color=BLACK)
pio.templates["blinkit"].layout.title.font = dict(family="Poppins, sans-serif", color=BLACK, size=18)
pio.templates.default = "blinkit"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Item Fat Content"] = df["Item Fat Content"].replace(
        {"LF": "Low Fat", "low fat": "Low Fat", "reg": "Regular"}
    )
    return df


df = load_data()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
st.sidebar.markdown(
    f"<div class='blinkit-badge' style='display:inline-block; margin-bottom:8px;'>"
    f"blink<span>it</span></div>",
    unsafe_allow_html=True,
)
st.sidebar.header("Filters")

outlet_types = st.sidebar.multiselect(
    "Outlet Type", sorted(df["Outlet Type"].unique()), default=list(df["Outlet Type"].unique())
)
location_tiers = st.sidebar.multiselect(
    "Outlet Location Tier",
    sorted(df["Outlet Location Type"].unique()),
    default=list(df["Outlet Location Type"].unique()),
)
fat_contents = st.sidebar.multiselect(
    "Item Fat Content",
    sorted(df["Item Fat Content"].unique()),
    default=list(df["Item Fat Content"].unique()),
)

filtered = df[
    df["Outlet Type"].isin(outlet_types)
    & df["Outlet Location Type"].isin(location_tiers)
    & df["Item Fat Content"].isin(fat_contents)
]

# ---------------------------------------------------------------------------
# Header + KPIs
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="blinkit-header">
        <div class="blinkit-badge">blink<span>it</span></div>
        <div>
            <p class="blinkit-title">Sales Performance Dashboard</p>
            <p class="blinkit-tagline">Delivering insights in minutes, not hours ⚡</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

total_sales = filtered["Sales"].sum()
average_sales = filtered["Sales"].mean()
number_of_items_sold = filtered["Sales"].count()
average_ratings = filtered["Rating"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales / 1_000:,.1f}K")
col2.metric("Average Sales", f"${average_sales:,.1f}")
col3.metric("Items Sold", f"{number_of_items_sold:,.0f}")
col4.metric("Average Rating", f"{average_ratings:,.1f} ⭐")

st.divider()

# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    sales_by_fat = filtered.groupby("Item Fat Content")["Sales"].sum().reset_index()
    fig = px.pie(
        sales_by_fat,
        names="Item Fat Content",
        values="Sales",
        title="Sales by Fat Content",
        hole=0.5,
        color_discrete_sequence=BRAND_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

with row1_col2:
    sales_by_size = filtered.groupby("Outlet Size")["Sales"].sum().reset_index()
    fig = px.pie(
        sales_by_size,
        names="Outlet Size",
        values="Sales",
        title="Sales by Outlet Size",
        hole=0.5,
        color_discrete_sequence=BRAND_SEQUENCE,
    )
    st.plotly_chart(fig, use_container_width=True)

sales_by_type = (
    filtered.groupby("Item Type")["Sales"].sum().sort_values(ascending=False).reset_index()
)
fig = px.bar(
    sales_by_type,
    x="Item Type",
    y="Sales",
    title="Total Sales by Item Type",
    text_auto=".2s",
    color_discrete_sequence=[YELLOW],
)
fig.update_traces(marker_line_color=BLACK, marker_line_width=1)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    sales_by_fat_outlet = (
        filtered.groupby(["Outlet Location Type", "Item Fat Content"])["Sales"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        sales_by_fat_outlet,
        x="Outlet Location Type",
        y="Sales",
        color="Item Fat Content",
        barmode="group",
        title="Fat Content by Outlet for Total Sales",
        color_discrete_sequence=[YELLOW, BLACK],
    )
    st.plotly_chart(fig, use_container_width=True)

with row2_col2:
    sales_by_location = (
        filtered.groupby("Outlet Location Type")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = px.bar(
        sales_by_location,
        x="Sales",
        y="Outlet Location Type",
        orientation="h",
        title="Sales by Outlet Location",
        color_discrete_sequence=[GREEN],
    )
    st.plotly_chart(fig, use_container_width=True)

sales_by_year = (
    filtered.groupby("Outlet Establishment Year")["Sales"].sum().sort_index().reset_index()
)
fig = px.line(
    sales_by_year,
    x="Outlet Establishment Year",
    y="Sales",
    markers=True,
    title="Total Sales by Outlet Establishment Year",
    color_discrete_sequence=[BLACK],
)
fig.update_traces(line_color=BLACK, marker=dict(color=YELLOW, size=10, line=dict(color=BLACK, width=1)))
st.plotly_chart(fig, use_container_width=True)

st.caption(f"Showing {len(filtered):,} of {len(df):,} rows after filters.")

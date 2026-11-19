"""
Sales Data Analytics Dashboard
Built with Streamlit, Plotly, and Pandas.
Professional Executive Portfolio Project.
"""

import os
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Executive Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (CSS)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 18px 22px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        color: #f8fafc;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25);
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        color: #38bdf8 !important;
    }

    /* Tab styling */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }

    /* Subtitle and headings */
    .dashboard-header {
        margin-bottom: 25px;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loading & Caching
# ---------------------------------------------------------
@st.cache_data
def load_sales_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_path = os.path.join(base_dir, "data", "cleaned_sales_data.csv")
    raw_path = os.path.join(base_dir, "data", "sales_data.csv")

    if os.path.exists(cleaned_path):
        df = pd.read_csv(cleaned_path)
    elif os.path.exists(raw_path):
        df = pd.read_csv(raw_path)
    else:
        st.error(f"Dataset not found! Expected at `{raw_path}`. Please run `python src/generate_data.py` first.")
        st.stop()

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    if "Profit Margin %" not in df.columns:
        df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)
    return df

try:
    df_raw = load_sales_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ---------------------------------------------------------
# Sidebar: Filters & Controls
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎯 Control Panel")
    st.caption("Sales Analytics & Portfolio Explorer")
    st.markdown("---")

    # Optional File Upload
    uploaded_file = st.file_uploader("📂 Upload Custom Sales CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df_raw = pd.read_csv(uploaded_file)
            df_raw["Order Date"] = pd.to_datetime(df_raw["Order Date"])
            if "Profit Margin %" not in df_raw.columns:
                df_raw["Profit Margin %"] = (df_raw["Profit"] / df_raw["Sales"] * 100).round(2)
            st.success("Custom dataset loaded!")
        except Exception as e:
            st.error(f"Error parsing uploaded file: {e}")

    # 1. Date Range Filter
    min_date = df_raw["Order Date"].min().date()
    max_date = df_raw["Order Date"].max().date()

    st.subheader("📅 Date Range")
    date_range = st.date_input(
        "Select Date Interval",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # 2. Region Filter
    all_regions = sorted(df_raw["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect("🌍 Region", options=all_regions, default=all_regions)

    # 3. Category Filter
    all_categories = sorted(df_raw["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect("📦 Product Category", options=all_categories, default=all_categories)

    # 4. Product Search / Filter
    all_products = ["All Products"] + sorted(df_raw["Product Name"].dropna().unique().tolist())
    selected_product = st.selectbox("🏷️ Specific Product", options=all_products)

    st.markdown("---")
    st.info(f"📊 **Total Database Records:** {len(df_raw):,}")

# ---------------------------------------------------------
# Apply Filters
# ---------------------------------------------------------
df_filtered = df_raw.copy()

# Date filter
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_d, end_d = date_range
    df_filtered = df_filtered[
        (df_filtered["Order Date"].dt.date >= start_d) &
        (df_filtered["Order Date"].dt.date <= end_d)
    ]

# Region filter
if selected_regions:
    df_filtered = df_filtered[df_filtered["Region"].isin(selected_regions)]

# Category filter
if selected_categories:
    df_filtered = df_filtered[df_filtered["Category"].isin(selected_categories)]

# Product filter
if selected_product != "All Products":
    df_filtered = df_filtered[df_filtered["Product Name"] == selected_product]

if df_filtered.empty:
    st.warning("⚠️ No data available matching the selected filter criteria. Please adjust your filters.")
    st.stop()

# ---------------------------------------------------------
# Dashboard Header
# ---------------------------------------------------------
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("📈 Sales Data Analysis Dashboard")
    st.markdown("Executive Business Overview & Commercial Performance Insights")
with col_h2:
    st.metric(
        label="Records Analyzed",
        value=f"{len(df_filtered):,}",
        delta=f"{(len(df_filtered)/len(df_raw)*100):.1f}% of Total"
    )

st.markdown("---")

# ---------------------------------------------------------
# KPI Cards Section
# ---------------------------------------------------------
total_revenue = df_filtered["Sales"].sum()
total_profit = df_filtered["Profit"].sum()
total_orders = df_filtered["Order ID"].nunique()
total_units = df_filtered["Quantity"].sum()
avg_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric(
    label="Total Revenue",
    value=f"${total_revenue:,.2f}",
    delta=f"AOV: ${total_revenue/total_orders:,.2f}" if total_orders else None
)
kpi2.metric(
    label="Total Profit",
    value=f"${total_profit:,.2f}",
    delta="Net Profit"
)
kpi3.metric(
    label="Total Orders",
    value=f"{total_orders:,}",
    delta=f"{df_filtered['Customer ID'].nunique():,} Customers"
)
kpi4.metric(
    label="Units Sold",
    value=f"{total_units:,}",
    delta="Total Volume"
)
kpi5.metric(
    label="Avg. Profit Margin",
    value=f"{avg_margin:.2f}%",
    delta="Target: >20%"
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Interactive Analytics Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Trends & Categories",
    "🌍 Regional & Products",
    "💡 Profit vs Sales Analysis",
    "📋 Raw Data & Export"
])

# ---------------------------------------------------------
# Tab 1: Trends & Categories
# ---------------------------------------------------------
with tab1:
    st.subheader("Monthly Performance Trends")
    
    # Group by Year-Month
    df_filtered["Year_Month"] = df_filtered["Order Date"].dt.strftime("%Y-%m")
    trend_df = df_filtered.groupby("Year_Month").agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index().sort_values(by="Year_Month")

    # Plotly Combined Line + Bar Chart
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=trend_df["Year_Month"],
        y=trend_df["Revenue"],
        name="Revenue ($)",
        marker_color="#38bdf8",
        opacity=0.85
    ))
    fig_trend.add_trace(go.Scatter(
        x=trend_df["Year_Month"],
        y=trend_df["Profit"],
        name="Profit ($)",
        mode="lines+markers",
        line=dict(color="#10b981", width=3),
        marker=dict(size=7)
    ))
    fig_trend.update_layout(
        title="Monthly Revenue vs Net Profit Trend",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=420
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        cat_df = df_filtered.groupby("Category").agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum")
        ).reset_index().sort_values(by="Revenue", ascending=False)

        fig_cat = px.bar(
            cat_df,
            x="Revenue",
            y="Category",
            orientation="h",
            text_auto=".2s",
            color="Profit",
            color_continuous_scale="Viridis",
            title="Revenue & Profit by Category",
            template="plotly_dark",
            height=360
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_t2:
        payment_df = df_filtered.groupby("Payment Mode").agg(
            Transactions=("Order ID", "count")
        ).reset_index()

        fig_pay = px.pie(
            payment_df,
            values="Transactions",
            names="Payment Mode",
            hole=0.45,
            title="Payment Mode Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template="plotly_dark",
            height=360
        )
        st.plotly_chart(fig_pay, use_container_width=True)

# ---------------------------------------------------------
# Tab 2: Regional & Products
# ---------------------------------------------------------
with tab2:
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.subheader("Regional Commercial Performance")
        reg_df = df_filtered.groupby("Region").agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum")
        ).reset_index().sort_values(by="Revenue", ascending=False)

        fig_reg = px.bar(
            reg_df,
            x="Region",
            y="Revenue",
            color="Profit",
            color_continuous_scale="Blues",
            title="Revenue and Profit Contribution by Region",
            text_auto=".2s",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with col_r2:
        st.subheader("Top 10 Best-Selling Products")
        top_prod = df_filtered.groupby("Product Name").agg(
            Revenue=("Sales", "sum"),
            Units=("Quantity", "sum")
        ).reset_index().sort_values(by="Revenue", ascending=False).head(10)

        fig_prod = px.bar(
            top_prod,
            x="Revenue",
            y="Product Name",
            orientation="h",
            color="Units",
            color_continuous_scale="Purples",
            title="Top 10 Products by Revenue",
            text_auto=".2s",
            template="plotly_dark",
            height=400
        )
        fig_prod.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_prod, use_container_width=True)

# ---------------------------------------------------------
# Tab 3: Profit vs Sales Analysis
# ---------------------------------------------------------
with tab3:
    st.subheader("Sales vs Profit Correlation & Margins")
    
    # Scatter plot of Sales vs Profit
    fig_scatter = px.scatter(
        df_filtered,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        hover_data=["Product Name", "Region", "Profit Margin %"],
        title="Transaction Scatter: Sales vs Net Profit",
        template="plotly_dark",
        height=500
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # City-level performance table
    st.markdown("### 🏙️ Top Performing Cities")
    city_df = df_filtered.groupby(["City", "Region"]).agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index()
    city_df["Profit_Margin_%"] = (city_df["Profit"] / city_df["Revenue"] * 100).round(2)
    city_df.sort_values(by="Revenue", ascending=False, inplace=True)
    st.dataframe(
        city_df.head(10).style.format({
            "Revenue": "${:,.2f}",
            "Profit": "${:,.2f}",
            "Profit_Margin_%": "{:.2f}%"
        }),
        use_container_width=True
    )

# ---------------------------------------------------------
# Tab 4: Raw Data & Export
# ---------------------------------------------------------
with tab4:
    st.subheader("Filtered Dataset Explorer")
    st.markdown("Inspect granular records and export filtered data for reports or presentations.")

    # Search filter
    search_query = st.text_input("🔍 Search by Customer ID, Order ID, or City", "")
    display_df = df_filtered
    if search_query:
        display_df = display_df[
            display_df["Customer ID"].str.contains(search_query, case=False, na=False) |
            display_df["Order ID"].str.contains(search_query, case=False, na=False) |
            display_df["City"].str.contains(search_query, case=False, na=False)
        ]

    st.dataframe(display_df.head(100), use_container_width=True)

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        csv_data = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="filtered_sales_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_d2:
        st.info("💡 For the complete multi-sheet Excel workbook with charts and KPI sheets, see `outputs/sales_analysis_report.xlsx`.")

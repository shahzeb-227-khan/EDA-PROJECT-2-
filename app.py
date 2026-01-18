import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from cleaning import (
    load_and_clean_data,
    revenue_by_country,
    top_products_by_revenue,
    monthly_sales_trend
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EDA PROJECT 2 : ONLINE RETAIL DASHBOARD",
    layout="wide",
    page_icon="📊"
)

sns.set_style("whitegrid")

# ---------------- LIGHT THEME CSS ----------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f6f9;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------
for key in ["country", "product", "monthly", "summary"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ---------------- LOAD DATA ----------------
df = load_and_clean_data("data/Online_Retail.csv")

country_rev = revenue_by_country(df)
product_rev = top_products_by_revenue(df)
monthly_sales = monthly_sales_trend(df).sort_values("Month")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Dashboard Controls")

if st.sidebar.button("🌍 Show Country Revenue"):
    st.session_state.country = True

if st.sidebar.button("📦 Show Product Revenue"):
    st.session_state.product = True

if st.sidebar.button("📈 Show Monthly Sales"):
    st.session_state.monthly = True

if st.sidebar.button("📉 Show Monthly Summary"):
    st.session_state.summary = True

# ---------------- TITLE ----------------
st.title("EDA PROJECT 2 : ONLINE RETAIL DASHBOARD")
st.markdown("### Exploratory Data Analysis • Cleaned Data • Interactive Insights")

st.divider()

# ---------------- CLEANED DATA PREVIEW ----------------
st.subheader("🔍 Cleaned Data Preview")
st.dataframe(df.head(20), width="stretch")

st.divider()

# ---------------- KPI METRICS ----------------
k1, k2, k3, k4 = st.columns(4)

k1.metric("💰 Total Revenue", f"${df['Amount'].sum():,.0f}")
k2.metric("📦 Orders", df["InvoiceNo"].nunique())
k3.metric("🌍 Countries", df["Country"].nunique())
k4.metric("🧑 Customers", df["CustomerID"].nunique())

st.divider()

# ================= DASHBOARD =================
st.subheader("📊 Sales Performance Dashboard")

# COMMON FIG SIZE (IMPORTANT)
FIG_SIZE = (7, 4)

# ---------- ROW 1 ----------
row1_col1, row1_col2 = st.columns(2)

if st.session_state.country:
    with row1_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🌍 Top 10 Countries by Revenue")

        fig, ax = plt.subplots(figsize=FIG_SIZE)
        sns.barplot(
            data=country_rev.head(10),
            x="Amount",
            y="Country",
            hue="Country",
            legend=False,
            palette="Blues_r",
            ax=ax
        )
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.product:
    with row1_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📦 Top 20 Products by Revenue")

        fig, ax = plt.subplots(figsize=FIG_SIZE)
        sns.barplot(
            data=product_rev,
            x="Amount",
            y="Description",
            hue="Description",
            legend=False,
            palette="Purples_r",
            ax=ax
        )
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- ROW 2 ----------
row2_col1, row2_col2 = st.columns(2)

if st.session_state.monthly:
    with row2_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📈 Monthly Revenue Trend")

        fig, ax = plt.subplots(figsize=FIG_SIZE)
        sns.lineplot(
            data=monthly_sales,
            x="Month",
            y="Amount",
            marker="o",
            color="#1f77b4",
            ax=ax
        )
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.summary:
    with row2_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📉 Top Revenue Months")

        top_months = (
            monthly_sales
            .sort_values("Amount", ascending=False)
            .head(10)
            .sort_values("Month")
        )

        fig, ax = plt.subplots(figsize=FIG_SIZE)
        sns.lineplot(
            data=top_months,
            x="Month",
            y="Amount",
            marker="o",
            color="#ff7f0e",
            ax=ax
        )
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= ENHANCED BUSINESS INSIGHTS =================
st.divider()
st.subheader("💡 Business Insights")

# Compute extra KPIs for insights
top_country = country_rev.iloc[0]["Country"]
top_country_revenue = country_rev.iloc[0]["Amount"]

top_product = product_rev.iloc[0]["Description"]
top_product_revenue = product_rev.iloc[0]["Amount"]

top_month = monthly_sales.sort_values("Amount", ascending=False).iloc[0]["Month"]
top_month_revenue = monthly_sales.sort_values("Amount", ascending=False).iloc[0]["Amount"]

total_revenue = df['Amount'].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_countries = df["Country"].nunique()

# Format cards to have same height using markdown + CSS
st.markdown(
    """
    <style>
    .insight-card {
        background-color: #d9f2e6;
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        height: 100%;
    }
    .insight-card-blue {
        background-color: #dce9fc;
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display insights side by side
i1, i2 = st.columns(2)

with i1:
    st.markdown(
        f"""
        <div class="insight-card">
        <h4>🌍 Market & Revenue Highlights</h4>
        <ul>
        <li><b>Top Country:</b> {top_country} (${top_country_revenue:,.0f})</li>
        <li><b>Top Product:</b> {top_product} (${top_product_revenue:,.0f})</li>
        <li><b>Peak Month:</b> {top_month} (${top_month_revenue:,.0f})</li>
        <li><b>Total Revenue:</b> ${total_revenue:,.0f}</li>
        <li><b>Total Orders:</b> {total_orders}</li>
        <li><b>Total Customers:</b> {total_customers}</li>
        <li><b>Total Countries:</b> {total_countries}</li>
        </ul>
        <p>These metrics show the key performance areas and highlight which markets and products are driving the most revenue. Monitoring these helps in strategy and inventory planning.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with i2:
    st.markdown(
        f"""
        <div class="insight-card-blue">
        <h4>📌 Observations & Recommendations</h4>
        <ul>
        <li>Revenue is highly concentrated in {top_country} — consider expanding marketing in emerging countries.</li>
        <li>{top_product} is the most profitable product — ensure stock levels are sufficient.</li>
        <li>{top_month} shows peak sales season — plan promotions around this month.</li>
        <li>Customer retention and loyalty programs can improve repeat purchases.</li>
        <li>Use this data for forecasting and demand planning to optimize inventory.</li>
        </ul>
        <p>Key trends indicate seasonal patterns, top-performing products, and geographic hotspots — perfect for data-driven decision-making.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

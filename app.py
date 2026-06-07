import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales & Revenue Analysis Dashboard")

df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year

st.sidebar.header("Filters")
year = st.sidebar.multiselect("Select Year", options=df['Year'].unique(), default=df['Year'].unique())
region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

filtered = df[(df['Year'].isin(year)) & (df['Region'].isin(region)) & (df['Category'].isin(category))]

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${filtered['Sales'].sum():,.0f}")
col2.metric("📈 Total Profit", f"${filtered['Profit'].sum():,.0f}")
col3.metric("🛒 Total Orders", f"{filtered['Order ID'].nunique():,}")
col4.metric("📦 Total Products", f"{filtered['Product Name'].nunique():,}")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Revenue Trend Over Time")
    trend = filtered.groupby(filtered['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    trend['Order Date'] = trend['Order Date'].astype(str)
    fig = px.line(trend, x='Order Date', y='Sales', markers=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sales by Category")
    cat_sales = filtered.groupby('Category')['Sales'].sum().reset_index()
    fig2 = px.pie(cat_sales, names='Category', values='Sales', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.subheader("Top 10 Products by Sales")
    top_products = filtered.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    fig3 = px.bar(top_products, x='Sales', y='Product Name', orientation='h', color='Sales')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Sales by Region")
    region_sales = filtered.groupby('Region')['Sales'].sum().reset_index()
    fig4 = px.bar(region_sales, x='Region', y='Sales', color='Region')
    st.plotly_chart(fig4, use_container_width=True)

st.caption("Sales Dashboard | Built with Python, Streamlit & Plotly")
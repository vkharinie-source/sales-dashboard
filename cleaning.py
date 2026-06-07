import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Data Cleaning & Reporting", layout="wide")
st.title("🧹 Data Cleaning & Reporting Automation")

# Load Data
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# --- BEFORE CLEANING ---
st.markdown("---")
st.subheader("📋 Before Cleaning - Data Issues Found")

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Total Rows", f"{len(df):,}")
col2.metric("❌ Missing Values", f"{df.isnull().sum().sum():,}")
col3.metric("🔁 Duplicate Rows", f"{df.duplicated().sum():,}")
col4.metric("📝 Total Columns", f"{len(df.columns):,}")

# Show raw data sample
st.subheader("Raw Data Sample (Before Cleaning)")
st.dataframe(df.head(10))

st.markdown("---")

# --- CLEANING PROCESS ---
st.subheader("🧹 Cleaning Process")

# Step 1: Remove duplicates
before_rows = len(df)
df_clean = df.drop_duplicates()
after_rows = len(df_clean)
duplicates_removed = before_rows - after_rows

# Step 2: Fill missing values
missing_before = df_clean.isnull().sum().sum()
df_clean = df_clean.fillna({
    col: df_clean[col].median() if df_clean[col].dtype in ['float64', 'int64']
    else df_clean[col].mode()[0] if not df_clean[col].mode().empty
    else 'Unknown'
    for col in df_clean.columns
})
missing_after = df_clean.isnull().sum().sum()

# Step 3: Strip whitespace
df_clean.columns = df_clean.columns.str.strip()
for col in df_clean.select_dtypes(include='object').columns:
    df_clean[col] = df_clean[col].str.strip()

# Show cleaning steps
col1, col2, col3 = st.columns(3)
col1.success(f"✅ Removed {duplicates_removed} duplicate rows")
col2.success(f"✅ Fixed {missing_before} missing values")
col3.success(f"✅ Cleaned whitespace in all columns")

st.markdown("---")

# --- AFTER CLEANING ---
st.subheader("✅ After Cleaning - Clean Data")

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Total Rows", f"{len(df_clean):,}")
col2.metric("✅ Missing Values", f"{df_clean.isnull().sum().sum():,}")
col3.metric("✅ Duplicate Rows", f"{df_clean.duplicated().sum():,}")
col4.metric("📝 Total Columns", f"{len(df_clean.columns):,}")

# Show clean data
st.subheader("Clean Data Sample (After Cleaning)")
st.dataframe(df_clean.head(10))

st.markdown("---")

# --- VISUAL SUMMARIES ---
st.subheader("📊 Visual Summaries")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    cat = df_clean.groupby('Category')['Sales'].sum().reset_index()
    fig1 = px.pie(cat, names='Category', values='Sales', hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Sales by Region")
    reg = df_clean.groupby('Region')['Sales'].sum().reset_index()
    fig2 = px.bar(reg, x='Region', y='Sales', color='Region')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- DOWNLOAD REPORT ---
st.subheader("📥 Download Clean Report")

# Excel Download
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df_clean.to_excel(writer, sheet_name='Clean Data', index=False)
    
st.download_button(
    label="📥 Download Clean Data as Excel",
    data=buffer.getvalue(),
    file_name="clean_report.xlsx",
    mime="application/vnd.ms-excel"
)

# CSV Download
csv = df_clean.to_csv(index=False)
st.download_button(
    label="📥 Download Clean Data as CSV",
    data=csv,
    file_name="clean_report.csv",
    mime="text/csv"
)

st.caption("Data Cleaning & Reporting | Built with Python, Streamlit & Pandas")
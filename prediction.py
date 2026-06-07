import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

st.set_page_config(page_title="Predictive Analytics", layout="wide")
st.title("🔮 Predictive Analytics Dashboard")

# Load Data
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Month'] = df['Order Date'].dt.to_period('M')

# Monthly Sales
monthly = df.groupby('Month')['Sales'].sum().reset_index()
monthly['Month_Num'] = range(len(monthly))
monthly['Month'] = monthly['Month'].astype(str)

# Train Model
X = monthly[['Month_Num']]
y = monthly['Sales']
model = LinearRegression()
model.fit(X, y)
monthly['Predicted'] = model.predict(X)

# Future Predictions
future_months = pd.DataFrame({'Month_Num': range(len(monthly), len(monthly)+6)})
future_sales = model.predict(future_months)
future_labels = pd.period_range(
    start=pd.Period(monthly['Month'].iloc[-1]) + 1,
    periods=6, freq='M'
).astype(str).tolist()

# Accuracy
mae = mean_absolute_error(y, monthly['Predicted'])
r2 = r2_score(y, monthly['Predicted'])

# KPI Cards
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Total Months", f"{len(monthly)}")
col2.metric("💰 Avg Monthly Sales", f"${y.mean():,.0f}")
col3.metric("🎯 Model Accuracy", f"{r2*100:.1f}%")
col4.metric("📉 Avg Error", f"${mae:,.0f}")

st.markdown("---")

# Chart 1 - Actual vs Predicted
st.subheader("📈 Actual vs Predicted Sales")
fig1 = px.line(monthly, x='Month', y=['Sales', 'Predicted'],
               title='Actual vs Predicted Sales Over Time')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# Chart 2 - Future Predictions
st.subheader("🔮 Future Sales Prediction (Next 6 Months)")
future_df = pd.DataFrame({
    'Month': future_labels,
    'Predicted Sales': future_sales
})
fig2 = px.bar(future_df, x='Month', y='Predicted Sales',
              color='Predicted Sales', title='Next 6 Months Sales Forecast')
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Chart 3 - Sales by Category Trend
st.subheader("📊 Sales Trend by Category")
cat_trend = df.groupby(['Month', 'Category'])['Sales'].sum().reset_index()
cat_trend['Month'] = cat_trend['Month'].astype(str)
fig3 = px.line(cat_trend, x='Month', y='Sales', color='Category',
               title='Category Sales Trend')
st.plotly_chart(fig3, use_container_width=True)

# Future Predictions Table
st.subheader("📋 Future Predictions Table")
st.dataframe(future_df)

st.caption("Predictive Analytics | Built with Python, Streamlit & Scikit-learn")
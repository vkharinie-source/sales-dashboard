import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("👥 Customer Segmentation Dashboard")

# Load Data
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# Prepare customer data
customer_df = df.groupby('Customer Name').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Orders=('Order ID', 'nunique'),
    Total_Profit=('Profit', 'sum')
).reset_index()

# Scale the data
scaler = StandardScaler()
X = scaler.fit_transform(customer_df[['Total_Sales', 'Total_Orders', 'Total_Profit']])

# KMeans Clustering
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
customer_df['Segment'] = kmeans.fit_predict(X)

# Label Segments
segment_labels = {0: '🔵 High Value', 1: '🟢 Regular', 2: '🟡 Low Activity', 3: '🔴 At Risk'}
customer_df['Segment Label'] = customer_df['Segment'].map(segment_labels)

# KPI Cards
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Customers", f"{len(customer_df):,}")
col2.metric("🔵 High Value", f"{len(customer_df[customer_df['Segment']==0]):,}")
col3.metric("🟢 Regular", f"{len(customer_df[customer_df['Segment']==1]):,}")
col4.metric("🔴 At Risk", f"{len(customer_df[customer_df['Segment']==3]):,}")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Segments Distribution")
    fig1 = px.pie(customer_df, names='Segment Label', title='Segments')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Sales vs Orders by Segment")
    fig2 = px.scatter(customer_df, x='Total_Orders', y='Total_Sales',
                      color='Segment Label', hover_data=['Customer Name'])
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Average Sales by Segment")
    avg_sales = customer_df.groupby('Segment Label')['Total_Sales'].mean().reset_index()
    fig3 = px.bar(avg_sales, x='Segment Label', y='Total_Sales', color='Segment Label')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Average Profit by Segment")
    avg_profit = customer_df.groupby('Segment Label')['Total_Profit'].mean().reset_index()
    fig4 = px.bar(avg_profit, x='Segment Label', y='Total_Profit', color='Segment Label')
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("Customer Data Table")
st.dataframe(customer_df[['Customer Name', 'Total_Sales', 'Total_Orders', 'Total_Profit', 'Segment Label']])

st.caption("Customer Segmentation | Built with Python, Streamlit, Scikit-learn & Plotly")
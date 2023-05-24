import streamlit as st

companies = ["SQM"]

# Title
st.title("Financial Prediction App")

# Select company
company = st.sidebar.selectbox("Company", companies)

# 
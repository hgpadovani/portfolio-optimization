import requests
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import json
import plotly.express as px
import plotly.graph_objects as go
from src.portfolio import Markowitz
pd.options.plotting.backend = "plotly"

st.set_option("deprecation.showfileUploaderEncoding", False)

st.title("Portfolio Optimization")
st.write("Disclaimer: This is an educational content only. Invest solely at your own risk.")
st.write("Portfolio optimization via Markowitz Efficient Frontier")
st.markdown("### << Fill parameters and dates first")


# User input value
st.sidebar.markdown("# Set up parameters")
selected_assets = st.sidebar.text_input("Tickers (separated by comma)", "VVAR3,RENT3,ITUB4")
value_to_invest = int(st.sidebar.text_input("Amount of money to invest", 50000))
min_value = int(st.sidebar.text_input("Minimum percentage to allocate (%)", 15))
iterations = int(st.sidebar.text_input("Number of portfolios to simulate", 10000))

# Selectiong date
st.sidebar.markdown("# Select valid dates")
st.sidebar.write("Must work for all tickers")
start_date = st.sidebar.date_input('Start date', datetime.datetime.now().date())
end_date = st.sidebar.date_input('End date', datetime.datetime.now().date())

# Getting assets right
selected_assets = selected_assets.split(',')
selected_assets = [asset.strip() for asset in selected_assets]
n_assets = len(selected_assets)
min_value = min_value / 100

# payload with dates
payload = {
    "start_date": str(start_date), 
    "end_date": str(end_date)
}

# displays a button
if st.button("Optimize Portfolio!"):
    df_full = pd.DataFrame()
    for ticker in selected_assets:
        if ticker is not None:
            res = requests.post(f"http://localhost:8000/get_data/{ticker}", json=payload)
            data = res.json()["data"]
            df = pd.DataFrame.from_dict(data, orient="index")
            df.index = pd.to_datetime(df.index)
            df.columns = [ticker]
        df_full = pd.concat([df_full, df], axis=1)

    fig = px.line(df_full, y=selected_assets)
    fig.update_layout(
            xaxis_title = "Time",
            yaxis_title = "Stock Price",
        )
    st.markdown("## Visualizing Stocks")
    st.plotly_chart(fig)

    # Initializing Markowitz Portfolio Optimization
    mk = Markowitz(df_full, selected_assets, value_to_invest, min_value)
    final_df, fig = mk.plot_efficient_frontier()

    st.markdown("## Optimal Allocation")
    st.dataframe(final_df)

    st.markdown("## The Efficient Frontier")
    st.plotly_chart(fig)
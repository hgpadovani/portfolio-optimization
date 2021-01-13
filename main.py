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

ASSETS = {
    "Via Varejo": "VVAR3.SA",
    "ITUB": "ITUB3.SA",
    "Magalu": "MGLU3.SA",
}

st.set_option("deprecation.showfileUploaderEncoding", False)

st.title("Portfolio Optimization")
st.write("Disclaimer: This is an educational content only. This IS NOT an official recommendation. Investing with this will be solely at your own risk.")
st.write("Portfolio optimization via Markowitz Efficient Frontier")

# User input value
value_to_invest = int(st.sidebar.text_input("Input the amount of money to invest", 10000))
iterations = int(st.sidebar.text_input("Number of simulated portfolios", 10000))

# Selecting assets for optimization
all_assets = [i for i in ASSETS.values()]
selected_assets = st.sidebar.multiselect(
    "Select a list of assets for optimization", list(all_assets), list(all_assets)
)
n_assets = len(selected_assets)

# Selectiong date
st.sidebar.write("Select dates")
start_date = st.sidebar.date_input('start date', datetime.datetime.now().date())
end_date = st.sidebar.date_input('end date', datetime.datetime.now().date())

# payload with dates
payload = {
    "assets": json.dumps(selected_assets),
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
    st.markdown("## Visualizing Stocks")
    st.plotly_chart(fig)

    # Initializing Markowitz Portfolio Optimization
    mk = Markowitz(df_full, selected_assets, value_to_invest)
    final_df, fig = mk.plot_efficient_frontier()

    st.markdown("## Optimal Allocation")
    st.dataframe(final_df)

    st.markdown("## The Efficient Frontier")
    st.plotly_chart(fig)
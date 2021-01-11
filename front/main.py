import requests
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import json


ASSETS = {
    "Via Varejo": "VVAR3.SA",
    "ITUB": "ITUB3.SA",
    "Magalu": "MGLU3.SA",
}

st.set_option("deprecation.showfileUploaderEncoding", False)

st.title("Asset management")

# Selecting asset for ploting
company = st.selectbox("Select an asset", [i for i in ASSETS.keys()])
ticker = ASSETS[company]

# Selecting assets for optimization
all_assets = [i for i in ASSETS.values()]
selected_assets = st.sidebar.multiselect(
    "Select a list of assets for optimization", list(all_assets), list(all_assets)
)

# Selectiong date
start_date = st.sidebar.date_input('start date', datetime.datetime.now().date())
end_date = st.sidebar.date_input('end date', datetime.datetime.now().date())

# payload with dates
payload = {
    "assets": json.dumps(selected_assets),
    "start_date": str(start_date), 
    "end_date": str(end_date)
}

# displays a button
if st.button("Plot Asset"):
    if ticker is not None:
        res = requests.post(f"http://localhost:8000/get_data/{ticker}", json=payload)
        data = res.json()["data"]
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.reset_index()
        df.columns = ["Date", "Adj_close"]
        fig, ax = plt.subplots()
        sns.lineplot(data=df, x='Date', y='Adj_close')
        #df.plot()
        st.pyplot(fig)

# displays a button
if st.button("Get all data"):
    if ticker is not None:
        res = requests.post(f"http://localhost:8000/get_data/get_full_data/{json.dumps(selected_assets)}", json=payload)
        data = res.json()["data"]
        print(data)

        # df = pd.DataFrame.from_dict(data, orient="index")
        # df.index = pd.to_datetime(df.index)
        # df = df.reset_index()
        # df.columns = ["Date", "Adj_close"]
        # fig, ax = plt.subplots()
        # sns.lineplot(data=df, x='Date', y='Adj_close')
        # #df.plot()
        # st.pyplot(fig)

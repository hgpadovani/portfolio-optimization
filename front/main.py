import requests
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime


ASSETS = {
    "Via Varejo": "VVAR3.SA",
    "ITUB": "ITUB3.SA",
    "Magalu": "MGLU3.SA",
}

st.set_option("deprecation.showfileUploaderEncoding", False)

st.title("Asset management")

# Selecting asset
company = st.selectbox("Select an asset", [i for i in ASSETS.keys()])
ticker = ASSETS[company]

# Selectiong date
start_date = st.sidebar.date_input('start date', datetime.datetime.now().date())
end_date = st.sidebar.date_input('end date', datetime.datetime.now().date())

# payload with dates
payload = {
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

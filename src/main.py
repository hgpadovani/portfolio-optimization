from fastapi import FastAPI
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
from typing import Dict
import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/get_data/{ticker}")
async def get_data(ticker: str, dates: Dict[str, str]):

    adj_close = data.DataReader(
        ticker, 
        start = dates["start_date"],
        end = dates["end_date"],
        data_source = 'yahoo'
    )['Adj Close']

    return {"data": adj_close}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


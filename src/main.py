from fastapi import FastAPI
import pandas as pd
import uvicorn
from pandas_datareader import data as web
import matplotlib.pyplot as plt
from typing import Dict
import datetime
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/get_data/{ticker}")
async def get_data(ticker: str, dates: Dict[str, str]):
    print(ticker)

    adj_close = web.DataReader(
        ticker, 
        start = dates["start_date"],
        end = dates["end_date"],
        data_source = 'yahoo'
    )['Adj Close']

    return {"data": adj_close}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


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
async def get_data(ticker: str, payload: Dict[str, str]):
    ticker = str(ticker)+".SA"
    adj_close = web.DataReader(
        ticker, 
        start = payload["start_date"],
        end = payload["end_date"],
        data_source = 'yahoo'
    )['Adj Close']

    return {"data": adj_close}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


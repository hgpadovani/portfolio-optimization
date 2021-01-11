import requests
import pandas as pd
import matplotlib.pyplot as plt

def collect_data(ticker, start_date, end_date):
    dates = {
        'start_date': start_date,
        'end_date': end_date
    }
    res = requests.post(f"http://backend:8000/get_data/{ticker}", files=dates)
    data = res.json()

final_data = []
for ticker in ["AAPL", "VVAR3.SA"]:
    data = collect_data(ticker, '01-01-2018', '01-12-2000')
    final_data.append(data)
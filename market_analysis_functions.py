import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_fetcher import burst_data_sucker
from data_fetcher import data_sucker
import datetime as dt
def market_day_stats(market: list[str]):
    timeframe = "1d"
    date = str(dt.date.today()).split("-")
    date.reverse()
    date[0] = str(int(date[0]) -1)
    date = "/".join(date)
    if len(market) == 0:
        print("No arguments given")
        return
    elif len(market) == 1:
        print(date)
        ticket = market[0].lower()
        data_sucker("1d", market[0], date)
        data_df = pd.read_csv(f"{ticket.upper()}-PERP_{timeframe}.csv")
        data_df.drop(columns={list(data_df)[0]: "Index"}, inplace=True)
        print(data_df)
    else:
        pass

def main():
    market_day_stats(["avax"])

if __name__ == "__main__":
    main()

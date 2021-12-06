import pandas as pd
import time
import ccxt
import datetime
exchange = ccxt.ftx()

def data_sucker(timeframe: str,market: str,start_date: str,start_time=None, created_csv_location = ".") -> pd.DataFrame:
    if start_time == None:
        if "m" in timeframe:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M"))
            fixedStartTime = time.mktime(datetime.datetime.strptime(start_date, "%d/%m/%Y %H:%M").timetuple())
        elif "h" in timeframe:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y %H"), "%d/%m/%Y %H"))
            fixedStartTime = time.mktime(datetime.datetime.strptime(start_date, "%d/%m/%Y %H").timetuple())
        else:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y"), "%d/%m/%Y"))
            fixedStartTime = time.mktime(datetime.datetime.strptime(start_date, "%d/%m/%Y").timetuple())
    else:
        if "m" in timeframe:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M"))
            sum_time = f"{start_date} {str(start_time)}"
            fixedStartTime = time.mktime(datetime.datetime.strptime(sum_time, "%d/%m/%Y %H:%M").timetuple())
        elif "h" in timeframe:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y %H"), "%d/%m/%Y %H"))
            sum_time = f"{start_date} {str(start_time)}"
            fixedStartTime = time.mktime(datetime.datetime.strptime(sum_time, "%d/%m/%Y %H").timetuple())
        else:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y"), "%d/%m/%Y"))
            sum_time = f"{start_date} {str(start_time)}"
            fixedStartTime = time.mktime(datetime.datetime.strptime(sum_time, "%d/%m/%Y").timetuple())
    df_ohlcv = pd.DataFrame(exchange.fetch_ohlcv(market.upper()+"-PERP", timeframe=timeframe, since=fixedStartTime*1000, limit=5000))
    df_ohlcv.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    while df_ohlcv["Date"].iloc[-1] < (date * 1000):
        df = pd.DataFrame(exchange.fetch_ohlcv(market.upper()+"-PERP", timeframe=timeframe, since=df_ohlcv["Date"].iloc[-1], limit=5000))
        df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        df_ohlcv = pd.concat([df_ohlcv, df], ignore_index=True)
    df_ohlcv.to_csv(f"{created_csv_location}/{market.upper()}-PERP_{timeframe}.csv")
    return df_ohlcv

def burst_data_sucker(timeframe: str,markets: list[str],start_date: str,start_time=None, created_csv_location= "."):
    if start_time == None:
        if "m" in timeframe:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M"))
        elif "h" in timeframe:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y %H"), "%d/%m/%Y %H"))
        else:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y"), "%d/%m/%Y"))
        fixedStartTime = time.mktime(datetime.datetime.strptime(start_date, "%d/%m/%Y").timetuple())
    else:
        if "m" in timeframe:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M"))
            sum_time = f"{start_date} {str(start_time)}"
            fixedStartTime = time.mktime(datetime.datetime.strptime(sum_time, "%d/%m/%Y %H:%M").timetuple())
        elif "h" in timeframe:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y %H"), "%d/%m/%Y %H"))
            sum_time = f"{start_date} {str(start_time)}"
            fixedStartTime = time.mktime(datetime.datetime.strptime(sum_time, "%d/%m/%Y %H").timetuple())
        else:
            date = datetime.datetime.timestamp(datetime.datetime.strptime(datetime.datetime.now().strftime("%d/%m/%Y"), "%d/%m/%Y"))
            sum_time = f"{start_date} {str(start_time)}"
            fixedStartTime = time.mktime(datetime.datetime.strptime(sum_time, "%d/%m/%Y").timetuple())
    for market in markets:
        df_ohlcv = pd.DataFrame(exchange.fetch_ohlcv(market.upper()+"-PERP", timeframe=timeframe, since=fixedStartTime*1000, limit=5000))
        df_ohlcv.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        while df_ohlcv["Date"].iloc[-1] < (date * 1000):
            df = pd.DataFrame(exchange.fetch_ohlcv(market.upper()+"-PERP", timeframe=timeframe, since=df_ohlcv["Date"].iloc[-1], limit=5000))
            df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
            df_ohlcv = pd.concat([df_ohlcv, df], ignore_index=True)
        df_ohlcv.to_csv(f"{created_csv_location}/{market.upper()}-PERP_{timeframe}.csv")


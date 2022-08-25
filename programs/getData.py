import datetime
import yfinance as yf

def getData(coin, days):
    today = datetime.date.today()
    d1 = today.strftime("%Y-%m-%d")
    d2 = datetime.date.today() - datetime.timedelta(days = days)
    d2 = d2.strftime("%Y-%m-%d")
    data = yf.download(coin, start = d2, end = d1, progress = False)
    return data
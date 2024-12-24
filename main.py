import yfinance as yf

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')  
    return data

ticker = input("Introduceti ticker-ul de bursa (ex: VUAA): ")
data = get_stock_data(ticker)
print(data)



from flask import Flask, render_template, request
import yfinance as yf
from datetime import datetime
import pytz

app = Flask(__name__)

def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    try:
        data = stock.history(start=start_date, end=end_date)
        if data.empty:
            return None, None, None, None
        open_price = data['Open'].iloc[0]
        close_price = data['Close'].iloc[-1]
        percentage_change = ((close_price - open_price) / open_price) * 100
    except Exception as e:
        return f"Eroare: {e}", None, None, None
    return data, open_price, close_price, percentage_change

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    open_price = None
    close_price = None
    percentage_change = None

    timezone = pytz.timezone('Europe/Bucharest')
    current_time = datetime.now(timezone)

    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        data, open_price, close_price, percentage_change = get_stock_data(
            ticker, start_date, end_date
        )

    return render_template(
        'index.html',
        data=data,
        open_price=open_price,
        close_price=close_price,
        percentage_change=percentage_change,
        current_time=current_time
    )

if __name__ == '__main__':
    app.run(debug=True)

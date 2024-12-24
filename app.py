from flask import Flask, render_template, request
import yfinance as yf
from datetime import datetime
import pytz

app = Flask(__name__)

def get_stock_data(ticker, start_date, end_date):
    """Obține datele bursiere pentru ticker-ul specificat între două date."""
    stock = yf.Ticker(ticker)
    try:
        data = stock.history(start=start_date, end=end_date)
        if data.empty:
            return None, None, None, None  # Returnează None dacă ticker-ul nu a fost găsit
        # Prețurile de deschidere și închidere
        open_price = data['Open'].iloc[0]  # Prețul de deschidere
        close_price = data['Close'].iloc[-1]  # Prețul de închidere
        # Calculăm procentul de schimbare
        percentage_change = ((close_price - open_price) / open_price) * 100  # Calculăm procentul
    except Exception as e:
        return f"Eroare: {e}", None, None, None  # Afișează mesajul de eroare
    return data, open_price, close_price, percentage_change

@app.route('/', methods=['GET', 'POST'])
def index():
    """Rotează pagina principală și gestionează cererile POST."""
    data = None
    open_price = None
    close_price = None
    percentage_change = None
    
    # Obține data și ora curentă în București
    timezone = pytz.timezone('Europe/Bucharest')
    current_time = datetime.now(timezone)  # Obține data și ora curentă în București
    
    if request.method == 'POST':
        ticker = request.form['ticker']  # Obține ticker-ul din formular
        start_date = request.form['start_date']  # Obține data de început
        end_date = request.form['end_date']  # Obține data de sfârșit
        print(f"Ticker primit: {ticker}, Data de început: {start_date}, Data de sfârșit: {end_date}")  # Debugging
        data, open_price, close_price, percentage_change = get_stock_data(ticker, start_date, end_date)  # Obține datele pentru ticker
        print(f"Data: {data}, Preț deschidere: {open_price}, Preț închidere: {close_price}, Procentaj: {percentage_change}")  # Debugging
    return render_template('index.html', data=data, open_price=open_price, close_price=close_price, percentage_change=percentage_change, current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True) 


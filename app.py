import datetime
import yfinance as yf
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if request.method == 'POST':
        coin = str(request.form.get('coin'))

        today = datetime.date.today()
        d1 = today.strftime("%Y-%m-%d")
        d2 = datetime.date.today() - datetime.timedelta(days = 9)
        d2 = d2.strftime("%Y-%m-%d")

        data = yf.download(coin, start = d2, end = d1, progress = False)
        data = data[['Close']]

        plt.plot(data['Close'])
        plt.xlabel("Date")
        plt.ylabel("Close")

        title = f'Last 10 days price of {coin}'
        plt.title(title)

        plt.savefig('./static/plot.png')

        return render_template('index.html', coin = coin)

app.run(debug=True)
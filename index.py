import datetime
import numpy as np
import yfinance as yf
from keras.models import load_model
from programs.candle_plot import candle_plot
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        coin = str(request.form.get('coin'))
        if coin == 'None':
            return render_template('index.html')

        else:
            if request.form.get('result') == "plot":
                    today = datetime.date.today()
                    d1 = today.strftime("%Y-%m-%d")
                    d2 = datetime.date.today() - datetime.timedelta(days = 9)
                    d2 = d2.strftime("%Y-%m-%d")
                    data = yf.download(coin, start = d2, end = d1, progress = False)
                    candle_plot(data)
                    return render_template('index.html', coin = coin)

            elif request.form.get('result') == 'predict':
                coin = str(request.form.get('coin'))
                coinDict = {
                    'BTC-USD' : 'bitcoin',
                    'DOGE-USD' : 'dogecoin',
                    'ETH-USD' : 'ethereum',
                    'MIOTA-USD' : 'iota',
                    'TRX-USD' : 'tron'
                }
                MODEL_PATH = f'./models/{coinDict[coin]}.h5'
                model = load_model(MODEL_PATH)

                today = datetime.date.today()
                d1 = today.strftime("%Y-%m-%d")
                d2 = datetime.date.today() - datetime.timedelta(days = 9)
                d2 = d2.strftime("%Y-%m-%d")

                new_sample = yf.download(coin, start = d2, end = d1, progress = False)
                last9 = new_sample[['Close']]
                vals = last9.values
                temp = []

                for i in range(len(vals)):
                    temp.append(vals[0][0])

                scaler = MinMaxScaler()

                sample = scaler.fit_transform(np.array(temp).reshape(-1, 1))
                sample = np.asarray(sample)[1:]
                sample = np.reshape(sample, (1, 1, 9))

                prediction = model.predict(sample, batch_size = 2)
                prediction = scaler.inverse_transform(prediction)

                return render_template('predict.html', prediction=prediction)

app.run(debug=True)
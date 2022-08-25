import datetime
import numpy as np
import yfinance as yf
from keras.models import load_model
from programs.candle_plot import candle_plot
from programs.scalePredict import scalePredict
from programs.getData import getData
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, render_template, request, flash

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
                    data = getData(coin, 9)
                    candle_plot(data)
                    return render_template('index.html', coin = coin)

            elif request.form.get('result') == 'predict':
                return render_template('predict.html')

@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    if request.method == 'POST':
        coin = str(request.form.get('coin'))
        if coin == 'None':
            return render_template('predict.html')
        else:
            if request.form.get('result') == 'day':
                COINS_DICT = {
                    'DOGE-USD': 'dogecoin',
                    'BTC-USD' : 'bitcoin',
                    'ETH-USD' :'ethereum'  ,
                    'MIOTA-USD' : 'iota',
                    'TRX-USD' : 'tron'
                }
                MODEL_PATH = f'./models/{COINS_DICT[coin]}.h5'
                model = load_model(MODEL_PATH)

                new_sample = getData(coin, 9)

                last9 = new_sample[['Close']]
                vals = last9.values
                temp = []
                for i in range(len(vals)):
                    temp.append(vals[0][0])

                prediction = scalePredict(temp, model)
                return render_template('predict.html', coin = coin, prediction = prediction)

            elif request.form.get('result') == 'week':
                COINS_DICT = {
                    'DOGE-USD': 'dogecoin',
                    'BTC-USD' : 'bitcoin',
                    'ETH-USD' :'ethereum'  ,
                    'MIOTA-USD' : 'iota',
                    'TRX-USD' : 'tron'
                }
                MODEL_PATH = f'./models/{COINS_DICT[coin]}.h5'
                model = load_model(MODEL_PATH)
                new_sample = getData(coin, 9)

                last9 = new_sample[['Close']]
                vals = last9.values
                temp = []
                for j in range(len(vals)):
                    temp.append(vals[0][0])

                for i in range(1, 8):
                    pred = scalePredict(temp, model)
                    temp = temp[1:]
                    temp.append(pred)

                prediction = scalePredict(temp, model)
                return render_template('predict.html', coin = coin, prediction = prediction)

            elif request.form.get('result') == 'fortnight':
                COINS_DICT = {
                    'DOGE-USD': 'dogecoin',
                    'BTC-USD' : 'bitcoin',
                    'ETH-USD' :'ethereum'  ,
                    'MIOTA-USD' : 'iota',
                    'TRX-USD' : 'tron'
                }
                MODEL_PATH = f'./models/{COINS_DICT[coin]}.h5'
                model = load_model(MODEL_PATH)

                new_sample = getData(coin, 9)
                last9 = new_sample[['Close']]
                vals = last9.values

                temp = []

                for i in range(len(vals)):
                    temp.append(vals[0][0])

                for i in range(1, 8):
                    pred = scalePredict(temp, model)
                    temp = temp[1:]
                    temp.append(pred)
                
                prediction = scalePredict(temp, model)
                return render_template('predict.html', coin = coin, prediction = prediction)

    return render_template('predict.html')

app.run(debug=True)
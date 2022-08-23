import joblib
import datetime
import numpy as np
import yfinance as yf

def prediction(scaler, coin):
  MODEL_PATH = f'/content/drive/MyDrive/model/{coin}.h5' 
  model = joblib.load(MODEL_PATH)
  coins_dict = {
    'dogecoin' : 'DOGE-USD',
    'bitcoin' : 'BTC-USD',
    'ethereum' : 'ETH-USD',
    'iota' : 'MIOTA-USD',
    'tron' : 'TRX-USD'
  }

  ticker = coins_dict[coin]

  today = datetime.date.today()
  d1 = today.strftime("%Y-%m-%d")
  d2 = datetime.date.today() - datetime.timedelta(days = 9)
  d2 = d2.strftime("%Y-%m-%d")

  new_sample = yf.download(ticker, start = d2, end = d1, progress = False)

  last9 = new_sample[['Close']]
  vals = last9.values

  temp = []

  for i in range(len(vals)):
    temp.append(vals[0][0])

  sample = scaler.fit_transform(np.array(temp).reshape(-1, 1))
  sample = np.asarray(sample)

  sample = np.reshape(sample, (1, 1, 9))

  prediction = model.predict(sample, batch_size = 2)

  prediction = scaler.inverse_transform(prediction)
  return prediction
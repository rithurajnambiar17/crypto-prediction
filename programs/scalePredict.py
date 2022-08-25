import numpy as np
from sklearn.preprocessing import MinMaxScaler

def scalePredict(temp, model):
    scaler = MinMaxScaler()
    sample = scaler.fit_transform(np.array(temp).reshape(-1,1))
    sample = np.asarray(sample)[:-1]
    sample = np.reshape(sample, (1,1,9))
    prediction = model.predict(sample, batch_size = 2)
    prediction = scaler.inverse_transform(prediction)
    return prediction
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime


def train_and_predict(dates, avg_temps):
    days_since_start = np.array([(date - dates[0]).days for date in dates]).reshape(-1, 1)
    avg_temps = np.array(avg_temps).reshape(-1, 1)

    model = LinearRegression()
    model.fit(days_since_start, avg_temps)

    next_day = np.array([[days_since_start[-1][0] + 1]])
    predicted_temp = model.predict(next_day)[0][0]

    return predicted_temp

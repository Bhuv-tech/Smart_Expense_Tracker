import numpy as np
from sklearn.linear_model import LinearRegression

def predict_next_month(months, totals):
    """
    months  → [1,2,3]
    totals  → [8000,9500,11000]
    """

    X = np.array(months).reshape(-1, 1)
    y = np.array(totals)

    model = LinearRegression()
    model.fit(X, y)

    next_month = max(months) + 1
    prediction = model.predict([[next_month]])

    return round(prediction[0], 2)
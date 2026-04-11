import joblib
import json
import numpy as np

model = joblib.load("../models/model.pkl")
scaler = joblib.load("../models/scaler.pkl")

with open("../models/columns.json") as f:
    columns = json.load(f)

with open("../models/threshold.txt") as f:
    threshold = float(f.read())

def predict(data_dict):
    arr = [data_dict.get(col, 0) for col in columns]
    arr = np.array([arr])
    arr = scaler.transform(arr)

    prob = model.predict_proba(arr)[0][1]
    return {
        "score": prob * 100,
        "selected": prob > threshold
    }
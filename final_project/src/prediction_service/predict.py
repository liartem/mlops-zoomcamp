import pickle
import pandas as pd
from sklearn.metrics import mean_absolute_error
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


with open('model.pkl', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


def predict(model, object):
    X = dv.transform(object)
    y_pred = model.predict(X)
    return float(y_pred)

def make_encoding(object):
    if list(object.items())[0][1] == "Male":
        object["Gender"] = "1"
    else:
        object["Gender"] = "0"
    return object

    
app = Flask("car-prediction")


@app.route('/predict', methods=['POST'])
def car_prediction():
    object = request.get_json()
    object = make_encoding(object)

    pred = predict(model, object)

    result = {
        'car-prediction': pred
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
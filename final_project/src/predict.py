import pickle
import pandas as pd
from sklearn.metrics import mean_absolute_error
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
from preprocess import make_label_encoding


with open('rf.pkl', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)

def prepare_features(event):
    features = {}
    features['Gender'] = event["Gender"]
    features['Age'] = event["Age"]
    features['Salary'] = event["Salary"]
    return features

def predict(model, features):
    X = dv.transform(features)
    y_pred = model.predict(X)
    return float(y_pred)


app = Flask("car-prediction")


@app.route('/predict', methods=['POST'])
def car_prediction():
    object = request.get_json()

    pred = predict(model, object)

    result = {
        'car-prediction': pred
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
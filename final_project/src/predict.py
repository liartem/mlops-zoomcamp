import pickle
import pandas as pd
from sklearn.metrics import mean_absolute_error
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


with open('rf.pkl', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


def predict(model, object):
    X = dv.transform(object)
    y_pred = model.predict(X)
    return float(y_pred)

def make_label_encoding(object):
    object = pd.DataFrame(object)
    le = LabelEncoder()
    object["Gender"] = le.fit_transform(object["Gender"])
    return object.to_json()

app = Flask("car-prediction")


@app.route('/predict', methods=['POST'])
def car_prediction():
    object = request.get_json()
    #object = make_label_encoding(object)

    pred = predict(model, object)

    result = {
        'car-prediction': pred
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
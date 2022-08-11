import pandas as pd
import numpy as np
import os
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

import matplotlib.pyplot as plt
import pickle
import mlflow



def train_model(train_df, train_target):
    model = RandomForestClassifier( n_estimators=100, n_jobs=-1, random_state=42 ).fit(train_df, train_target)
    print("training is complete")
    return model

def save_model(model, dv):
    with open('model.pkl', 'wb') as f_out:
        pickle.dump((dv,model), f_out)

def make_label_encoding(df):
    encoder = LabelEncoder()
    df["Gender"] = encoder.fit_transform(df["Gender"])
    return df

def make_dict_victorizer(train_df, test_df):
    dv = DictVectorizer()
    train_dicts = train_df.to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)

    test_dicts = test_df.to_dict(orient='records')
    X_test = dv.transform(test_dicts)
    return X_train, X_test, dv

def calculate_metrics(model, X_test, test_target):
    y_pred_test = model.predict(X_test)
    accuracy = accuracy_score(test_target, y_pred_test)
    precision = precision_score(test_target, y_pred_test) 
    recall = recall_score(test_target, y_pred_test)
    f1 = f1_score(test_target, y_pred_test)
    metrics_dict = {"accuracy" : accuracy, "precision" : precision, "recall" : recall, "f1" : f1}
    return metrics_dict


mlflow.set_tracking_uri("sqlite:///final_project.db")
mlflow.set_experiment("car-prediction-experiment")

if __name__ == '__main__':
    with mlflow.start_run():

        mlflow.set_tag("developer", "Artem")
        
        df = pd.read_csv(r"../data/car_data.csv")
        df = make_label_encoding(df)
        X = df[["Gender", "Age", "AnnualSalary"]]
        y = df["Purchased"]

        random_state = 42
        train_df, test_df, train_target, test_target = train_test_split(X, y, test_size = 0.33, random_state=random_state)

        mlflow.log_param("random state", random_state)
        
        X_train, X_test, dv = make_dict_victorizer(train_df, test_df)

        model = train_model(X_train, train_target)

        # metrics calculation
        metrics_dict = calculate_metrics(model, X_test, test_target)
        mlflow.log_metrics(metrics_dict)

        save_model(model, dv)


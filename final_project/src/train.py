import pandas as pd
import numpy as np
import os
import sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import pickle
from preprocess import make_label_encoding



def train_model(train_df, train_target):
    model = RandomForestRegressor( n_estimators=100, n_jobs=-1, random_state=42 ).fit(train_df, train_target)
    print("training is complete")
    return model

def save_model(model, dv):
    with open('model.pkl', 'wb') as f_out:
        pickle.dump((dv,model), f_out)


if __name__ == '__main__':
    df = pd.read_csv(r"../data/car_data.csv")
    df, dv = make_label_encoding(df)
    X = df[["Gender", "Age", "AnnualSalary"]]
    y = df["Purchased"]
    train_df, test_df, train_target, test_target = train_test_split(X, y, test_size = 0.33)
    model = train_model(train_df, train_target)
    save_model(model, dv)




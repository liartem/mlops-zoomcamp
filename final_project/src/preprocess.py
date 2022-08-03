import pandas as pd
import numpy as np
import os
import sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.feature_extraction import DictVectorizer


import matplotlib.pyplot as plt
import pickle

sys.path.insert(0, os.path.abspath('../data/'))

df = pd.read_csv(r"../data/car_data.csv")

def make_label_encoding(df):
    
    encoder = LabelEncoder()
    df["Gender"] = encoder.fit_transform(df["Gender"])

    return df






if __name__ == '__main__':

    df, dv = make_label_encoding(df)




import pandas as pd
import numpy as np
import os
import sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

import matplotlib.pyplot as plt
import pickle

sys.path.insert(0, os.path.abspath('../data/'))

df = pd.read_csv(r"C:\Users\leear\Desktop\Python\mlops-zoomcamp\final_project\data\PJME_hourly.csv")

def sort_by_date_and_time(df) -> pd.DataFrame:
    
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.sort_values(by=['Datetime'], axis=0, ascending=True, inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df


def interpolate_and_fill_missing_vales(df):

    df.rename(columns={df.columns[1] : "consumption"}, inplace=True)
    df = df.set_index('Datetime')
    df["consumption"].interpolate(method='linear', inplace=True)
    return df


def create_time_features(df):

    df['dow'] = df.index.dayofweek # day of week
    df['doy'] = df.index.dayofyear # day of year
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['quarter'] = df.index.quarter
    df['hour'] = df.index.hour
    df['dom'] = df.index.day # Day of Month
    df['date'] = df.index.date 
    df.reset_index(inplace=True, drop=True)
    return df


def time_series_train_test_split(df):
    
    min_year = df.year.min()
    max_year = df.year.max()
    print(f"min year = {min_year}, max year = {max_year}")

    train_percent = 0.75
    time_between = max_year - min_year
    train_cutoff = min_year + train_percent*time_between
    
    train_df = df[df.year <= train_cutoff].drop(columns=["consumption", "date"])
    train_target = df[df.year <= train_cutoff]["consumption"]
    test_df = df[df.year > train_cutoff].drop(columns=["consumption", "date"])
    test_target = df[df.year > train_cutoff]["consumption"]
    return train_df, train_target, test_df, test_target


def train_model(train_df, train_target):
    model = RandomForestRegressor( n_estimators=100, n_jobs=-1, random_state=42 ).fit(train_df, train_target)
    print("training is complete")
    return model

def save_model(model):
    pickle.dump(model, open("model.pkl", 'wb'))

def predict(model, test_df, test_target):
    y_pred_test = model.predict(test_df)
    mae = mean_absolute_error(test_target, y_pred_test)
    plt.plot(test_df.index, y_pred_test, test_target)
    plt.savefig("pic1.png")
    print(f"mae = {mae}")



if __name__ == '__main__':
    df = sort_by_date_and_time(df)
    df = interpolate_and_fill_missing_vales(df)
    df = create_time_features(df)
    train_df, train_target, test_df, test_target = time_series_train_test_split(df)
    model = train_model(train_df, train_target)
    save_model(model)



import pandas as pd
import datetime 
import time
import pickle
import mlflow

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner

@task
def read_data(path):
    df = pd.read_parquet(path)
    return df

@task
def prepare_features(df, categorical, train=True):
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    mean_duration = df.duration.mean()
    if train:
        print(f"The mean duration of training is {mean_duration}")
    else:
        print(f"The mean duration of validation is {mean_duration}")
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

@task
def train_model(df, categorical):

    train_dicts = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts) 
    y_train = df.duration.values

    print(f"The shape of X_train is {X_train.shape}")
    print(f"The DictVectorizer has {len(dv.feature_names_)} features")

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_train)
    mse = mean_squared_error(y_train, y_pred, squared=False)
    print(f"The MSE of training is: {mse}")
    return lr, dv

@task
def run_model(df, categorical, dv, lr):
    val_dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(val_dicts) 
    y_pred = lr.predict(X_val)
    y_val = df.duration.values

    mse = mean_squared_error(y_val, y_pred, squared=False)
    print(f"The MSE of validation is: {mse}")

    return

@task
def get_paths(date):
    if date is None:
        date = datetime.datetime.today()
        train_month = date.month-2
        valid_month = date.month-1
    else:
        train_month =  int(date[6]) -2
        valid_month =  int(date[6]) -1

    train_path = str(f"./data/fhv_tripdata_2021-0{train_month}.parquet")
    val_path = str(f"./data/fhv_tripdata_2021-0{valid_month}.parquet")
    return train_path, val_path

@flow(task_runner=SequentialTaskRunner())
def main(date = "2021-08-15"):

    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("nyc-taxi-experiment")

    train_path, val_path = get_paths(date).result()

    categorical = ['PUlocationID', 'DOlocationID']

    df_train = read_data(train_path)
    df_train_processed = prepare_features(df_train, categorical)

    df_val = read_data(val_path)
    df_val_processed = prepare_features(df_val, categorical, False)

    # train the model
    lr, dv = train_model(df_train_processed, categorical).result()

    run_model(df_val_processed, categorical, dv, lr)

    with mlflow.start_run():

        mlflow.sklearn.log_model(lr, artifact_path="models", registered_model_name = f"model-{date}")

        with open(f"artifacts_local/dv-{date}.b", "wb") as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact(f"artifacts_local/dv-{date}.b", artifact_path="models")

#deployment section
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule 
from prefect.flow_runners import SubprocessFlowRunner
from datetime import timedelta

DeploymentSpec(
    flow=main,
    name="cron-schedule-deployment",
    schedule=CronSchedule(
        cron="0 9 15 * *",
        timezone="Europe/Zurich"),
    flow_runner=SubprocessFlowRunner(),
    tags=["homework", "CronSchedule"]
)


main()

import pandas as pd
import requests
from catboost import CatBoostRegressor
import mlflow
import boto3
import uuid

from prefect import task, flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner, ConcurrentTaskRunner
from prefect.context import get_run_context

def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids


def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df['ride_id'] = generate_uuids(len(df))

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts


def load_model(run_id):
    logged_model = f's3://mlflow-models-artem/1/{run_id}/artifacts/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model


def save_results(df, y_pred, run_id, output_file):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    #df_result['model_version'] = run_id

    df_result.to_parquet(output_file, index=False)

@flow(task_runner=SequentialTaskRunner())
def run(url, path, output_file, run_id):
    
    logger = get_run_logger()    

    logger.info(f'downloading data from , {url}')
    data = read_dataframe(url)

    logger.info('creating dictionaries')
    dicts = prepare_dictionaries(data)

    logger.info(f'loading the model from {path}')
    model = load_model(run_id)

    logger.info('making the predictions')
    y_pred = model.predict(dicts)

    logger.info(f'saving the results to the {output_file}')
    save_results(data, y_pred, run_id, output_file)


def main():
    month = 1
    year = 2020
    taxi_type = "green"

    run_id = '8824f6b0be88476895aa907644154a2b'
    path = f's3://mlflow-models-artem/1/{run_id}/artifacts/model'
    url = f's3://nyc-tlc/trip data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f's3://nyc-duration-prediction-artem/taxi_type={taxi_type}/year={year}/month={month}.parquet'
    run(url, path, output_file, run_id)

if __name__=='__main__':
    main()
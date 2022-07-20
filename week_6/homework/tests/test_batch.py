import os
import sys

sys.path.append("/home/ubuntu/mlops-zoomcamp/06-best-practices/homework")
from batch import main, prepare_data

import pandas as pd
from datetime import datetime
from deepdiff import DeepDiff


def test_batch():

    actual_result = main(2021, 2)
    expected_result = 1
    assert actual_result == expected_result

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)
    

def test_prepare_data():

    data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
    ]

    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categorical = ['PUlocationID', 'DOlocationID']
    actual_output = prepare_data(df, categorical)

    print(f"actual output = ", actual_output)

    expected_output = f's3://nyc-duration-prediction-artem/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    difference = DeepDiff(expected_output, actual_output)
    print(f'diff = {difference}')
    assert actual_output == expected_output



import pickle
import pandas as pd
import sys





with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)


def read_data(filename, categorical) -> pd.DataFrame:
    df = pd.read_parquet(filename)
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy() 
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df


def make_predictions(df, categorical, year, month) -> pd.DataFrame:

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    print(y_pred.mean())

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df_result = df.copy()
    df_result["y_pred"] = y_pred
    df_result = df_result[["ride_id", "y_pred"]]
    return df_result


def write_output(df_result, output_file):
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

def run(year, month, taxi_type, output_file, categorical):
    df = read_data(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet', categorical)
    df_result = make_predictions(df, categorical, year, month)
    write_output(df_result, output_file)
    print("done")

def main():
    year = int(sys.argv[1]) #2021
    month = int(sys.argv[2])
    taxi_type = 'fhv'
    output_file =  f'./{taxi_type}/{year:04d}-{month:02d}.parquet'
    categorical = ['PUlocationID', 'DOlocationID']

    run(year, month, taxi_type, output_file, categorical)
    

if __name__=="__main__":
    main()


import argparse
import os
import pickle
import mlflow
import mlflow.sklearn


from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def run(data_path):

        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        mlflow.set_experiment("homework-2")
        mlflow.sklearn.autolog()

        with mlflow.start_run():

            mlflow.set_tag("type", "homework")
            mlflow.set_tag("model", "rf-regressor")

            #mlflow.log_param("train-data-path", "./data/green_tripdata_2021-01.parquet")
            #mlflow.log_param("valid-data-path", "./data/green_tripdata_2021-02.parquet")
            X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
            X_valid, y_valid = load_pickle(os.path.join(data_path, "valid.pkl"))

            rf = RandomForestRegressor(max_depth=10, random_state=0)
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_valid)

            rmse = mean_squared_error(y_valid, y_pred, squared=False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default="./output",
        help="the location where the processed NYC taxi trip data was saved."
    )
    args = parser.parse_args()

    run(args.data_path)

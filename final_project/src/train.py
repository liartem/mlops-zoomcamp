import pickle
import random
from datetime import datetime

import numpy as np
import mlflow
import pandas as pd
import matplotlib.pyplot as plt
from prefect import flow, task
from mlflow.tracking import MlflowClient
from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from prefect.task_runners import SequentialTaskRunner
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer


@task
def train_model(train_df, train_target):
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42).fit(
        train_df, train_target
    )
    print("training is complete")
    return model


@task
def save_model(model, dv):
    '''
    Saves the new version of a model to the prediction_service/model.pkl
    '''
    with open('prediction_service/model.pkl', 'wb') as f_out:
        pickle.dump((dv, model), f_out)


def make_label_encoding(df):
    '''
    Makes label encoding for categorical feature,
    returns 1 when Gender == "Male" and 0 when "Female"
    '''
    encoder = LabelEncoder()
    df_encoded = df.copy()
    df_encoded["Gender"] = encoder.fit_transform(df["Gender"])
    return df_encoded


@task
def make_dict_victorizer(train_df, test_df):
    '''
    Uses dictionary vectorizer for processing the dictionaries
    '''
    dv = DictVectorizer()
    train_dicts = train_df.to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)

    test_dicts = test_df.to_dict(orient='records')
    X_test = dv.transform(test_dicts)
    return X_train, X_test, dv


@task
def calculate_metrics(model, X_test, test_target):
    '''
    Calculates the accuracy, precision, recall and f1 score metrics for a test data
    '''
    y_pred_test = model.predict(X_test)
    accuracy = accuracy_score(test_target, y_pred_test)
    precision = precision_score(test_target, y_pred_test)
    recall = recall_score(test_target, y_pred_test)
    f1 = f1_score(test_target, y_pred_test)
    metrics_dict = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }
    return metrics_dict


@task
def save_test_dataset(df, test_target):
    '''
    Rewrites test dataset in ./evidently_service/datasets/
    '''
    test_df = df.loc[test_target.index]
    test_df.to_csv("./evidently_service/datasets/test.csv", index=False)
    print("dataset is saved")


MLFLOW_TRACKING_URI = "sqlite:///final_project.db"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("car-prediction-experiment")


@flow(task_runner=SequentialTaskRunner())
def run():
    with mlflow.start_run() as run:

        client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
        run_id = run.info.run_id
        model_uri = f"runs:/{run_id}/model"
        model_name = "car-prediction-model"
        mlflow.set_tag("developer", "Artem")

        df = pd.read_csv(r"../data/car_data.csv")
        df_encoded = make_label_encoding(df)

        random_state = random.randint(1, 100)
        print(f"random state = {random_state}")
        X = df_encoded[["Gender", "Age", "AnnualSalary"]]
        y = df_encoded["Purchased"]
        train_df, test_df, train_target, test_target = train_test_split(
            X, y, test_size=0.33, random_state=random_state
        )

        mlflow.log_param("random state", random_state)

        X_train, X_test, dv = make_dict_victorizer(train_df, test_df)

        model = train_model(X_train, train_target)

        # metrics calculation
        metrics_dict = calculate_metrics(model, X_test, test_target)
        mlflow.log_metrics(metrics_dict)

        save_model(model, dv)
        mlflow.sklearn.log_model(model, artifact_path="models")
        mlflow.log_artifacts(local_dir="artifacts")
        mlflow.register_model(model_uri=model_uri, name=model_name)

        client.transition_model_version_stage(
            name=model_name,
            version=1,
            stage="Production",
            archive_existing_versions=False,
        )
        save_test_dataset(df, test_target)


if __name__ == '__main__':
    run()

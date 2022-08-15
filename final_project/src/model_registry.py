import pickle
import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime
from mlflow.entities.model_registry.model_version import ModelVersion
from mlflow.entities.model_registry._model_registry_entity import _ModelRegistryEntity
import pandas as pd

MLFLOW_TRACKING_URI = f"sqlite:///final_project.db"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("car-prediction-experiment")

if __name__ == '__main__':

    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
    date = datetime.today().date()
    new_stage = "Production"
    model_name= "car-prediction-model"

    #get current production model 
    for model_version in  client.search_model_versions("name='car-prediction-model'"):
        if model_version.current_stage == "Production":
            prod_model = model_version
    run_id_current = prod_model.run_id
    print(f"run_id_current={run_id_current}")

    current_run = client.get_run(run_id=run_id_current)
    current_accuracy = current_run.data.metrics["accuracy"]
    print(f"current accuracy = ", current_accuracy)

    #get the best model
    best_run = client.search_runs(
        experiment_ids='1',
        filter_string="metrics.accuracy > 0.85", 
        order_by=["metrics.accuracy.ASC"]
    ) [1]

    best_run_id = best_run.info.run_id
    print(f"best_run_id={best_run_id}")
    best_accuracy = best_run.data.metrics["accuracy"]
    print(f"best accuracy = ", best_accuracy)

    for model_version in client.search_model_versions("name='car-prediction-model'"):
        if model_version.run_id == best_run_id:
            version = model_version.version
    
    print(f"version = {version}")

    if best_accuracy > current_accuracy:

        client.transition_model_version_stage(
            name=model_name,
            version = version, 
            stage=new_stage,
            archive_existing_versions=True
    )
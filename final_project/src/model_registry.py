import pickle
import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime

MLFLOW_TRACKING_URI = f"sqlite:///final_project.db"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("car-prediction-experiment")

def get_current_model_parameters():
    '''
    get the current parameters of a registered model in production
    '''
    for model_version in client.search_model_versions("name='car-prediction-model'"):
        if model_version.current_stage == "Production":
            prod_model = model_version
            run_id_current = prod_model.run_id
            current_run = client.get_run(run_id=run_id_current)
            current_accuracy = current_run.data.metrics["accuracy"]
        else: # if there is no model in production
            current_accuracy = 0
            run_id_current = 0

    print(f"run_id_current={run_id_current}")
    print(f"current accuracy = ", current_accuracy)
    return run_id_current, current_accuracy


def get_best_model_parameters():
    '''
    get the parameters of the best trained model
    '''
    best_run = client.search_runs(
        experiment_ids='1',
        filter_string="metrics.accuracy > 0.85", 
        order_by=["metrics.accuracy.ASC"]
    ) [1]

    best_run_id = best_run.info.run_id
    best_accuracy = best_run.data.metrics["accuracy"]
    
    print(f"best_run_id={best_run_id}")
    print(f"best accuracy = ", best_accuracy)

    for model_version in client.search_model_versions("name='car-prediction-model'"):
        if model_version.run_id == best_run_id:
            version = model_version.version
    return best_run_id, best_accuracy, version
    

if __name__ == '__main__':

    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
    date = datetime.today().date()
    new_stage = "Production"
    model_name= "car-prediction-model"

    run_id_current, current_accuracy = get_current_model_parameters()
    best_run_id, best_accuracy, version = get_best_model_parameters()

    if best_accuracy > current_accuracy:
        client.transition_model_version_stage(
            name=model_name,
            version = version, 
            stage=new_stage,
            archive_existing_versions=True
    )
        print(f"version registered = {version}")

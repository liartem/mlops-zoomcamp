from prefect import flow
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner

from train import run

@flow
def myflow():
    print("hello world")

Deployment(
    flow=run,
    name="car-prediction-model",
    schedule=CronSchedule(cron="5 4 1 * *"), # At 04:05 on day-of-month 1 
    flow_runner=SubprocessFlowRunner(),
    tags=["final_project"]
)
print("success")


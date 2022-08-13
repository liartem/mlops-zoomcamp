from prefect import flow

@flow
def myflow():
    print("hello")

from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner

Deployment(
    flow=myflow,
    name="car-prediction-model",
    schedule=CronSchedule(cron="5 4 1 * *"), # At 04:05 on day-of-month 1 
    flow_runner=SubprocessFlowRunner(),
    tags=["final_project"]
)


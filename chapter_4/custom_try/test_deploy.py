from prefect.deployments import DeploymentSpec as DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner
from prefect import flow

DeploymentSpec(
    flow_location="test.py",
    name="play_with_prefect", 
    schedule=CronSchedule(cron="5 * * * *"),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml"]
)

if __name__=="__main__":
    DeploymentSpec()
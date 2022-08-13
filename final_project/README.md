Project
<h1> Project description</h1>

This is the implementation of final project for the course mlops-zoomcamp from DataTalksClub https://github.com/DataTalksClub/mlops-zoomcamp.
The project provides the online service for the prediction of customers intention to buy a car. The dataset has been taken from kaggle: https://www.kaggle.com/code/ehetshamshaukat/car-purchase-decision-analysis-and-model/data.
The main focus of the project is to make a **production** service with experiment tracking, pipeline automation, observability rather than building "the best" model for prediction. 

Run mlflow:
mlflow ui --backend-store-uri sqlite:///final_project.db 
mlflow server --backend-store-uri sqlite:///final_project.db --default-artifact-root ./artifacts

[2022-08-13 09:57:37 +0000] [17633] [ERROR] Connection in use: ('127.0.0.1', 5000)
[2022-08-13 09:57:37 +0000] [17633] [ERROR] Retrying in 1 second.

pkill gunicorn


settings -> privacy and security -> clean cash



prefect config set PREFECT_ORION_UI_API_URL="http://35.172.212.237:4200/api", where 35.172.212.237 is an ip address of remote server
prefect config set PREFECT_API_URL=http://0.0.0.0:4200/api
prefect orion start --host 0.0.0.0


prefect deployment create schedule_deployment.py - deployment creation

then the work queue should be created, then prefect agent should pick the work queue by command: 
prefect agent start 5f5bfd27-2567-4989-8b34-c83f61f81684
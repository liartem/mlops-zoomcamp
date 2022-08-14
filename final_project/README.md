<h1> Project description</h1>

This is the implementation of final project for the course mlops-zoomcamp from DataTalksClub https://github.com/DataTalksClub/mlops-zoomcamp. <br/>
The project provides the **online service** for the prediction of customers intention to buy a car. The dataset has been taken from kaggle: https://www.kaggle.com/code/ehetshamshaukat/car-purchase-decision-analysis-and-model/data. The given input features for the model are Gender, Age and AnnualSalary. In responce service give a prediction for a particular customer, whether he is intended to buy a car (1) or not (0). <br/>
The main focus of the project is to make a **production** service with experiment tracking, pipeline automation, observability rather than building "the most accurate" prediction model. <br/>

<h1> Technical details</h1>
The project is implemented on Ubuntu 22.04 on Amazon AWS. The described steps for reproducbility are based on specific AWS configuration and may be different based on the production platform (GCP, Azure, locally, and so on). The instruction about reproducibility of a project can be found in **how_to_reproduce.md** file <br/>
This repository has 2 folders: _ src _  and *data*. The folder *data* contains the whole dataset for the given service. Due to the small size of dataset, it is located directly in git. In the folder *src* the man source code is provided with various configuration files for docker  and existing databases. <br/>

Mlflow is used as a main instrument for experiment tracking and model registry. The results of experiment are saved to the final_project.db in src folder. Also, the model registry is used for registering and the changing the stage of the models. <br/>

Prefect has been used as a main workflow orchestrator in this project. The training pipeline is automated and can be deployed with different time intervals. <br/>

The observability of the service is provided by combination of Grafana, Prometheus and Evidently. Is has information about the possible data drift, categorical target drift and should provide report for classification performance. <br/>

<h1> Demo </h1>

The small demo below aims to show the main functionality of a service. It starts by running docker-compose, send the objects to Flask application from send_data.py, and ensires observability in Grafana with help of Evidently dashboards. 

![demo ](https://user-images.githubusercontent.com/54916420/184533951-d26b2ede-da27-4e14-bebc-a8821daaba1b.gif)


![system design](https://user-images.githubusercontent.com/54916420/184542992-5186f4d4-7992-46a2-9172-5e91aa78e3b9.jpg)


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

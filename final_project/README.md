![system design car prediction service Artem Li](https://user-images.githubusercontent.com/54916420/184544310-790e099a-1dec-4d10-8d1f-44e730c5f4ee.JPG)

<h1> Project description</h1>

This is the implementation of final project for the course mlops-zoomcamp from [DataTalksClub](https://github.com/DataTalksClub/mlops-zoomcamp). <br/>
The project provides the **online service** for the prediction of customers intention to buy a car. The dataset has been taken from [kaggle](https://www.kaggle.com/code/ehetshamshaukat/car-purchase-decision-analysis-and-model/data). Let's imagine that the aim is to predict a customer's intention to buy a car. The given input features for the model are Gender, Age and AnnualSalary. In responce service give a prediction for a particular customer, whether he is intended to buy a car (1) or not (0). <br/>
The main focus of the project is to make a **production** service with experiment tracking, pipeline automation, observability rather than building "the most accurate" prediction model. <br/>

<h1> Technical details and high-level overview</h1>

The project is implemented on Ubuntu 22.04 on Amazon AWS. The described steps for reproducbility are based on specific AWS configuration and may be different based on the production platform (GCP, Azure, locally, and so on). The instruction about reproducibility of a project can be found in the actual readme. <br/>

This repository has 2 folders: *src*  and *data*. The folder *data* contains the whole dataset for the given service. Due to the small size of dataset, it is located directly in git. In the folder *src* the main source code is provided with various configuration files for docker and existing databases. The folder *.github/workflow" of the CORE directory contains the configuration files for CI/CD pipeline. CI pipeline makes unit and integration tests (linters were disabled), CD pipeline makes a image of application and pushed it to docker hub. <br/>

### High-level overview

*The picture with "system design" can be used in order to understand the working schema of a current project.* <br/>

The script *train.py* is used as a main code for fetching the input data, creating of a model, promoting it to the model registry and saving as pickle file. [Mlflow](https://mlflow.org/) is used as a main instrument for experiment tracking and model registry. The results of experiment are saved to the final_project.db. <br/>

The script *schedule_deployment.py* is used for the scheduling the deployment of a model. [Prefect](https://www.prefect.io/) has been used as a main workflow orchestrator in this project. The training pipeline is automated and can be deployed with different time intervals. <br/>

After the model is trained, the whole application can be started by running docker compose file (see step 3). It runs the Flask application  with a service that has current model and ensures observability by a combination of [Grafana](https://grafana.com/), [Prometheus](https://prometheus.io/) and [Evidently](https://github.com/evidentlyai). Is provides information in real time about the possible model's performance, such as data drift and categorical target drift.

The simulation of traffic is done in *send_data.py* script. It sends input features in JSON format, such as Gender, Age and AnnualSalary to the service with time difference of 1 second. In responce, service gives an prediction for a given customer about his intention to buy a car (1) or not (0).

<h1> Demo </h1>

The small demo below aims to show the main functionality of a service. It starts by running docker-compose, send the objects to Flask application from send_data.py, and ensires observability in Grafana with help of Evidently dashboards. 

![demo ](https://user-images.githubusercontent.com/54916420/184533951-d26b2ede-da27-4e14-bebc-a8821daaba1b.gif)

<h1> Quick start </h1>

##### Step 0
Create a Virtual Machine. It is recommended to refer to [this video](https://www.youtube.com/watch?v=IXSiYkP23zo&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&index=3&ab_channel=DataTalksClub%E2%AC%9B) and create similar AWS EC2 instance. The reproducibility has been proved only in EC2 instance, making the same steps in another cloud provider or locally may cause unexpected bugs.<br/>

##### Step 1
copy [this](https://github.com/liartem/mlops-zoomcamp) .git folder by running 
```
https://github.com/liartem/mlops-zoomcamp.git
```

##### Step 2
Navigate into the *src* repository and run:
```
pipenv shell
```
It should install all required dependencies and activate the working environment. **scr environment should be activated always when running some commands**

##### Step 3
After the pipenv environment is activated, the whole application can be started by running 
```
docker-compose up --build
```
##### Step 4
In order to simulate the production service and send data to the running Flask application, the following command should be written: 
```
python send_data.py
```
It reads the rows from *test.csv* file and send it to the Flask application. In responce, service will outputs the predictions 1 or 0, what corresponds the prediction for a customer to buy a car (1) or not (0). 

##### Step 5
In order to ensure observability of a given service, it is possible to reach Grafana on
```
http://localhost:3000/
```
Ideally, all given metrics should be updated in real time with providing additional information. <br/>
Hint: do not forgot to make a port mapping. 

![port mapping](https://user-images.githubusercontent.com/54916420/184546076-e465e10e-3692-4d2c-958a-1697bcc6eea6.png) <br/>
Steps 2-4 are shown in the presented demo. 

##### Step 6
All previous steps are used for **starting** the service, in order to **change** some parts of a service or prove its functionality, the steps described below can be run.
For example, training the new model can be done by running 

```
python train.py
```
This script takes the input data, randomly choose random state, performs train test split, make a encoding of categorical feature (Gender), save dictionary vectorizer and model.pkl files. Since model training happends every time on a similar dataset, there should be a small difference in performance metrics. <br/>
In order to see experiment tracking, MlFlow should be started by: 

```
mlflow server --backend-store-uri sqlite:///final_project.db --default-artifact-root ./artifacts
```
The user interface can be achieved on: 
```
http://localhost:5000/
```
If mlflow shows error, such as <br/>


* \[2022-08-13 09:57:37 +0000\] \[17633\] \[ERROR\] connection in use: ('127.0.0.1', 5000) * <br/>
* \[2022-08-13 09:57:37 +0000\] \[17633\] \[ERROR\] Retrying in 1 second. * <br/>

The command should be run <br/>

```
pkill gunicorn
```

Also it can be helpful to clean the browser cash, such as <br/>

```
settings -> privacy and security -> clean cash
```

##### Step 7

This service has an automated workflow and Prefect is used as a main workflow orchestrator. In order to start Prefect, the followed commands should be written: 
```
prefect config set PREFECT_ORION_UI_API_URL="http://<external ip>:4200/api", where <external ip> is an ip address of a remote server
prefect config set PREFECT_API_URL=http://0.0.0.0:4200/api
prefect orion start --host 0.0.0.0
```

The deployment is managed in file *schedule_deployment.py*, originally it has a Cron schedule, but can be changed for different version. 

```
prefect deployment create schedule_deployment.py 
```

then the work queue should be created, then prefect agent should pick the work queue by command: 

```
prefect agent start 5f5bfd27-2567-4989-8b34-c83f61f81684 
```
where the 5f5bfd27-2567-4989-8b34-c83f61f81684 is a unique identifier of a queue


# Possibility for improvement

The current project has some oppoptunities for improvements, for example: <br/>

1) Add the possibility to retrain the model and send an alert, when the data/target drift are detected. 

2) Add IaC


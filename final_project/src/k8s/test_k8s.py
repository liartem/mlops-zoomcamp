import requests

object = {
        "Gender": "Male",
        "Age": 20,
        "AnnualSalary": 1000,
        }

url = 'http://af263b3f02d7d41229ed9ae70fce1ea8-1249848547.eu-west-1.elb.amazonaws.com:80/predict' # change the name of the service when restarted
response = requests.post(url, json=object)
print(response.json())
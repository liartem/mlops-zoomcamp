import requests

event = {
        "Gender": "Male",
        "Age": 30,
        "AnnualSalary": 100000,
        }

url = 'http://localhost:9696/predict'
response = requests.post(url, json=event)
print(response.json())
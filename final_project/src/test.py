import requests

object = {
        "Gender": "Male",
        "Age": 20,
        "AnnualSalary": 1000,
        }

url = 'http://localhost:9696/predict'
response = requests.post(url, json=object)
print(response.json())
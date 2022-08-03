import requests

object = {
        "Gender": "Male",
        "Age": 50,
        "AnnualSalary": 100000,
        }

url = 'http://localhost:9696/predict'
response = requests.post(url, json=object)
print(response.json())
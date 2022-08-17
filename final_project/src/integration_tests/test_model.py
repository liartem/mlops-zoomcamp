import json
import requests


def integration_test():
    '''
    Test a model.pkl from src/prediction_service/predict.py
    raise an AssertionError if the prediction isn't correct
    Hint: it starts by a different dockerfile located in current directory
    '''

    row = {
            "Gender": "Male",
            "Age": 20,
            "AnnualSalary": 1000,
            }
            
    URL = "http://localhost:9696/predict"
    response = requests.post(URL, json=row)

    actual_response = response.json()
    print(actual_response)

    expected_response = {'car-prediction': 0.0}
    assert expected_response == actual_response

if __name__=='__main__':
    integration_test()
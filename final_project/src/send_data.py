import json
from datetime import datetime
from time import sleep
import pyarrow as pa


import pandas as pd
import requests

table = pd.read_csv("./evidently_service/datasets/test.csv")
table = pa.Table.from_pandas(table, preserve_index=True)
data  = table.to_pylist() 


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


with open("target.csv", 'w') as f_target:
    for row in data:
        # sends the data to the prediction service with 1 second pause
        f_target.write(f"{row['User ID']},{row['Purchased']}\n")
        resp = requests.post("http://127.0.0.1:9696/predict",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(row, cls=DateTimeEncoder)).json()
        print(f"prediction: {resp['car-prediction']}")
        sleep(1)

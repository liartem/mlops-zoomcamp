# syntax=docker/dockerfile:1

FROM python:3.9.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install evidently==0.1.51.dev0

COPY app.py .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8085"]
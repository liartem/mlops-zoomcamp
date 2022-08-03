FROM python:3.9.12

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile" , "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "rf.pkl", "./"]

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
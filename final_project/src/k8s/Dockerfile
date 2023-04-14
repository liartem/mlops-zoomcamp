FROM python:3.9.12

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY requirements.txt requirements.txt

COPY [ "Pipfile" , "Pipfile.lock", "./"]

#RUN pipenv install --system --deploy

RUN pip3 install -r requirements.txt

COPY ["predict.py", "model.pkl", "./"]
COPY "model.pkl" .

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
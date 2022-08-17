FROM python:3.9.12

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY requirements.txt requirements.txt

COPY [ "Pipfile" , "Pipfile.lock", "./"]

RUN pip3 install -r requirements.txt

COPY predict.py . 
COPY model.pkl .

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9696"]

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
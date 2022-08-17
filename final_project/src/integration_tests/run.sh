#!/usr/bin/env bash

docker-compose up --build -d

sleep 5

pipenv run python test_model.py

docker-compose down

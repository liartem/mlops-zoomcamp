#!/usr/bin/env bash

cd "$(dirname "$0")"

docker-compose up --build -d

sleep 5

pipenv run python test_model.py

docker-compose down

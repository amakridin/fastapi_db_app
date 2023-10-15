#!/bin/bash

source .venv/bin/activate
pip3 install -r requirements.txt
gunicorn --config python:src.apps.api.gunicorn

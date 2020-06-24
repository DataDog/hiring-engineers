#!/usr/bin/env bash

virtualenv venv
source ./venv/bin/activate

pip3 install flask
pip3 install -v ddtrace

echo
echo "running flask app ... (in the foreground to see what's going on)"
DD_SERVICE=custom_flask_app FLASK_APP=custom_flask_app.py flask run --port=5533

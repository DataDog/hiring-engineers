#!/usr/bin/env bash

# Baseline
export DD_HOSTNAME=$VM_HOSTNAME
export DD_HOST_TAGS=role:demo:api,interviewee:john@jrichter.io

cd /vagrant
bash provisioning/baseline.sh

# Host setup
mkdir /opt/demo_api
cp provisioning/demo_api/demo_api.env /opt/demo_api/
cp provisioning/demo_api/demo_api.service /etc/systemd/system/

# Create the Python virtual environment
cd /opt/demo_api
sudo apt-get install -y python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-pip python3-venv
python3 -m venv venv

# Setup the demo_api virtual environment
source venv/bin/activate
pip install wheel Cython
pip install -r /app/requirements.txt
deactivate

# Permissions
chown -R vagrant:vagrant /opt/demo_api

# Start services
sudo systemctl start demo_api
sudo systemctl enable demo_api
bash /vagrant/provisioning/start.sh

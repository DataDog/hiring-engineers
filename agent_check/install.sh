#!/bin/bash
# Installs MongoDB and the Datadog integration
# This script is to be executed manually from inside the vagrant VM
# @Author: Chris Kelner (@ckelner)

set -ex
SCRIPT_NAME="$(basename ${0})"
PARENT_DIR=$(pwd)

sudo cp /vagrant_data/agent_check/randomcheck.py /etc/dd-agent/checks.d/
sudo cp /vagrant_data/agent_check/randomcheck.yaml /etc/dd-agent/conf.d/

sudo /etc/init.d/datadog-agent restart

sudo -u dd-agent dd-agent check randomcheck

#!/usr/bin/env bash

# Baseline
export DD_HOSTNAME=$VM_HOSTNAME
export DD_HOST_TAGS=role:web,interviewee:john@jrichter.io

cd /vagrant
bash provisioning/baseline.sh

# Host setup


# Start services
bash provisioning/start.sh

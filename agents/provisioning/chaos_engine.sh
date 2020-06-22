#!/usr/bin/env bash

# Baseline
export DD_API_KEY
export DD_HOSTNAME=$VM_HOSTNAME
export DD_HOST_TAGS=role:chaos,interviewee:john@jrichter.io

cd /vagrant
bash provisioning/baseline.sh

# Host setup
cp -R provisioning/chaos_engine/chaos_engine.d /etc/datadog-agent/conf.d/
chown -R dd-agent:dd-agent /etc/datadog-agent/conf.d/chaos_engine.d

cp /app/datadog_agent_checks/* /etc/datadog-agent/checks.d/
chown -R dd-agent:dd-agent /etc/datadog-agent/checks.d/*

# Start services
bash provisioning/start.sh

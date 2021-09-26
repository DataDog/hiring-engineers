#!/bin/bash

# Restart the agent
systemctl restart datadog-agent

# Scheduling is done by the below cron job:
# @reboot sudo watch -n 45 /usr/local/bin/ddagent-restart.sh

#!/usr/bin/env bash

echo "bootstrap.sh 1: allow apt to install through https"
sudo apt-get update
sudo apt-get install apt-transport-https

echo "bootstrap.sh 2: set up the Datadog deb repo on system and import Datadog's apt key"
sudo sh -c "echo 'deb https://apt.datadoghq.com/ stable 6' > /etc/apt/sources.list.d/datadog.list"
sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 382E94DE

echo "bootstrap.sh 3: install the Agent"
sudo apt-get update
sudo apt-get install datadog-agent

echo "bootstrap.sh 4: copy the example config and plug in API key from .env"
source .env
echo "api key: $DATADOG_API_KEY"
sudo sh -c "sed 's/api_key:.*/api_key: $DATADOG_API_KEY/' /etc/datadog-agent/datadog.yaml.example > /etc/datadog-agent/datadog.yaml"

echo "bootstrap.sh 5: give agent tags"
# this could be probably be abstracted out
# have the tags come from a file so different instances don't need individual agent_bootstraps
sudo sed -i 's/# tags:.*/tags: role:database, region:us/' /etc/datadog-agent/datadog.yaml

echo "boostrap.sh 6: start the datadog agent"
sudo initctl start datadog-agent


#!/usr/bin/env bash

export DD_API_KEY
export TWITTER_CONSUMER_KEY
export TWITTER_CONSUMER_SECRET
export TWITTER_ACCESS_TOKEN
export TWITTER_ACCESS_SECRET
export DD_HOSTNAME=$VM_HOSTNAME
export DD_HOST_TAGS=role:data-collection,interviewee:john@jrichter.io

# Baseline

cd /vagrant
bash provisioning/baseline.sh
sed -i 's/# apm_config:/apm_config:/' /etc/datadog-agent/datadog.yaml
sed -i 's/# apm_non_local_traffic: false/apm_non_local_traffic: true/' /etc/datadog-agent/datadog.yaml

# Host setup
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

usermod -a -G docker dd-agent
cp -R provisioning/twitter_collector/docker.d /etc/datadog-agent/conf.d/
chown -R dd-agent:dd-agent /etc/datadog-agent/conf.d/docker.d

cd provisioning/twitter_collector
docker build -t twitter_collector .

# Start services
docker stop twitter_collector
docker rm twitter_collector
docker run -d --restart=unless-stopped -p 8080:8080 --name twitter_collector -e DD_AGENT_HOST=172.16.1.12 -e DD_AGENT_APM_PORT=8126 -e DD_API_KEY -e TWITTER_CONSUMER_KEY -e TWITTER_CONSUMER_SECRET -e TWITTER_ACCESS_TOKEN -e TWITTER_ACCESS_SECRET twitter_collector
bash ../start.sh

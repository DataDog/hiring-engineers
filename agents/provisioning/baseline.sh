#!/usr/bin/env bash

export DD_AGENT_MAJOR_VERSION=7
export DD_INSTALL_ONLY=true

apt-get update
apt-get upgrade --no-install-recommends -y
apt-get install python3

bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
sed -i 's/# env: <environment name>/env: development:local/' /etc/datadog-agent/datadog.yaml
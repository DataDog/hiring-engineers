#!/bin/bash
# Install the Datadog agent on the local host.

if [ -z "$1" ]; then
  echo "Usage: $0 YOURAPIKEY"
fi

KEY=$1

# Dog-ify the MOTD
cp /home/ubuntu/bits.txt /etc/motd

# Render the Datadog config file
mkdir /etc/datadog
cat <<EOM > /etc/datadog/datadog.yaml
api_key: $KEY
EOM

# Fetch and install the agent
wget https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh -O /tmp/install_script.sh
chmod +x /tmp/install_script.sh
DD_API_KEY=$KEY DD_AGENT_MAJOR_VERSION=7 DD_INSTALL_ONLY=true /tmp/install_script.sh

# To Dos:
# Add tags in the agent config file
# Install PostgreSQL and agent integration https://www.datadoghq.com/blog/collect-postgresql-data-with-datadog/
# Create a custom agent check https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

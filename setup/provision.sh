#!/usr/bin/env bash

# provision all the software we need in our Vagrant host


API_KEY=2fcab63f3a5b4647d684977366b68cd8
#db478d2f1f0a8b79c7396b99b3f5181a
DD_PG_USER_PASSWORD=dd_pg_integration

# refresh package index
apt-get update

# need curl to install the agent
apt-get install -y curl

# get pip3
sudo apt-get install -y python3-pip

pip3 install virtualenv

echo 'put the config/check files into place'
echo
mkdir -p /etc/datadog-agent/conf.d/postgres.d
mkdir -p /etc/datadog-agent/checks.d
cp /vagrant/config/datadog.yaml /etc/datadog-agent/
cp /vagrant/config/conf.yaml /etc/datadog-agent/conf.d/postgres.d/
cp /vagrant/config/custom_my_check.yaml /etc/datadog-agent/conf.d/
cp /vagrant/config/custom_my_check.py /etc/datadog-agent/checks.d/
echo


# postgres
apt-get install -y postgresql postgresql-contrib

sudo -u postgres psql -c "create user datadog with password '${DD_PG_USER_PASSWORD}';"
sudo -u postgres psql -c "grant SELECT ON pg_stat_database to datadog;"

# datadog agent
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=${API_KEY} DD_SITE="datadoghq.eu" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
echo

# run the tracing app
cd /vagrant/apm
./run_app.sh

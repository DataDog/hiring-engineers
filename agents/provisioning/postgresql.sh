#!/usr/bin/env bash

############
# Baseline #
############

export DD_HOSTNAME=$VM_HOSTNAME
export DD_HOST_TAGS=role:storage,interviewee:john@jrichter.io
DD_PSQL_USER=datadog
DD_PSQL_PASSWORD=datadog
PSQL_DATABASE=postgres
PSQL_LOG_PATH=/var/log/postgresql/postgresql.log

cd /vagrant
bash provisioning/baseline.sh

##############
# Host setup #
##############

# Install and configure postgresql
apt-get install -y postgresql postgresql-contrib
cp provisioning/postgresql/postgres.conf /etc/postgresql/10/main/postgresql.conf
cp provisioning/postgresql/pg_hba.conf /etc/postgresql/10/main/pg_hba.conf
chmod ugo+r /etc/postgresql/10/main/*.conf
chown postgres:postgres /etc/postgresql/10/main/*.conf
service postgresql restart

sudo -u postgres psql -v dduser=${DD_PSQL_USER} -v ddpassword=${DD_PSQL_PASSWORD} -d postgres -f provisioning/postgresql/configure_psql.sql

# Enable Datadog postgres integration
sed -i 's/# logs_enabled: false/logs_enabled: true/' /etc/datadog-agent/datadog.yaml

cp provisioning/postgresql/dd_postgres.yaml /etc/datadog-agent/conf.d/postgres.d/conf.yaml
sed -i "s/<DD_PSQL_USER>/${DD_PSQL_USER}/" /etc/datadog-agent/conf.d/postgres.d/conf.yaml
sed -i "s/<DD_PSQL_PASSWORD>/${DD_PSQL_PASSWORD}/" /etc/datadog-agent/conf.d/postgres.d/conf.yaml
sed -i "s/<DD_PSQL_DATABASE>/${PSQL_DATABASE}/" /etc/datadog-agent/conf.d/postgres.d/conf.yaml
sed -i "s#<DD_PSQL_LOG_PATH>#${PSQL_LOG_PATH}#" /etc/datadog-agent/conf.d/postgres.d/conf.yaml
sed -i "s/<HOSTNAME>/${VM_HOSTNAME}/" /etc/datadog-agent/conf.d/postgres.d/conf.yaml
chmod ugo+r /etc/datadog-agent/conf.d/postgres.d/conf.yaml
chown dd-agent:dd-agent /etc/datadog-agent/conf.d/postgres.d/conf.yaml

##################
# Start services #
##################

bash provisioning/start.sh

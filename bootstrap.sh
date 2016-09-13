#!/usr/bin/env bash

hostname rich-centos

sudo yum update -y
sudo yum install postgresql-server -y

sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

DD_API_KEY=276e4b8abbe9988ee1ba1371c87e71b3 DD_INSTALL_ONLY=true bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
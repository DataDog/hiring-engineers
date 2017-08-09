#!/bin/bash
mkdir datadog
cd datadog

vagrant init hashicorp/precise64
vagrant up

vagrant ssh -c 'sudo apt-get -y update'
vagrant ssh -c 'sudo apt-get -y install apache2 mysql'
vagrant ssh -c 'sudo apt-get install mysql-server'
vagrant ssh -c 'sudo apt-get -y install php5 libapache2-mod-php5 php5-mcrypt'
vagrant ssh -c 'DD_API_KEY=de9281ea7641dc5b0e61641c5eef1f50 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"'

vagrant ssh


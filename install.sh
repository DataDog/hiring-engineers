#!/bin/bash
mkdir datadog
cd datadog

vagrant init hashicorp/precise64
vagrant up

vagrant ssh -c 'sudo apt-get -y update'
vagrant ssh -c 'sudo apt-get -y install curl apache2'
vagrant ssh -c 'sudo apt-get -y install mysql-server mongodb'
vagrant ssh -c 'sudo apt-get -y install php5 libapache2-mod-php5 php5-mcrypt'
vagrant ssh -c 'DD_API_KEY=API_KEY_GOES_HERE bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"'

vagrant ssh

#!/bin/bash
mkdir datadog
cd datadog

vagrant init hashicorp/precise64
vagrant up

vagrant ssh -c 'sudo apt-get -y update'
vagrant ssh -c 'sudo apt-get -y install curl apache2 mysql'
vagrant ssh -c 'sudo apt-get -y install mysql-server mongodb'
vagrant ssh -c 'sudo apt-get -y install php5 libapache2-mod-php5 php5-mcrypt'
vagrant ssh -c 'DD_API_KEY=API_KEY_GOES_HERE bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"'

vagrant ssh

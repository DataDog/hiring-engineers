#!/bin/bash
# Installs MongoDB and the Datadog integration
# This script is to be executed manually from inside the vagrant VM
# @Author: Chris Kelner (@ckelner)

set -ex
SCRIPT_NAME="$(basename ${0})"
PARENT_DIR=$(pwd)

# Install mongo
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# check all is well
tail -n 10 /var/log/mongodb/mongod.log

# NOTE: passwords should always be treated with utmost care and never checked
# into source control and kept in some kind of secrets management
# this is for demo purposes only and simplicity sake
pwd="AgEIqb6Kl35II2F2bXWuqIWg"
# allow command to fail -- allows script to be "idempotent-ish"
# this way the script can be run multiple times and if the user already exists
# then it will continue until completion
set +e
# NOTE: default admin credentials should be changed; for demo purposes only
mongo admin --eval "db.createUser({'user':'datadog', 'pwd': '$pwd', 'roles' : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})"

set -e # exit on failure -- next commands will check user actually exists

# check that it is working
echo "db.auth('datadog', '$pwd')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" &&
echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"

sudo tee /etc/dd-agent/conf.d/mongo.yaml > /dev/null <<EOF
init_config:

instances:
  - server: mongodb://datadog:$pwd@localhost:27017
    tags:
      - kelnerrox
      - kelnerhax
EOF

sudo /etc/init.d/datadog-agent restart
# TODO: Refactor: bad hack; but allows user to see checks running after script
# is done running
sleep 20 # wait for checks to kick off
sudo /etc/init.d/datadog-agent info

#!/bin/bash
echo "MongoDB Install Script - v4.4 - Started"

echo "Installing Repo"
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

echo "Installing Binaries"
sudo apt-get update
sudo apt-get install -y mongodb-org

echo "Start MongoDB"
sudo systemctl start mongod
sudo systemctl status mongod

sleep 5

mongo admin <<'EOF'
use admin

exit
EOF

sleep 5

echo "Mongo Shell: Adding admin & datadog user, create db, insert my_metric"
mongo admin <<'EOF'
use admin

var user = {
  "user" : "admin",
  "pwd" : "admin",
  roles : [
      {
          "role" : "userAdminAnyDatabase",
          "db" : "admin"
      },
      "readWriteAnyDatabase" 
  ]
}
db.createUser(user);

use admin
db.auth("admin", "admin");

var ddUser = {
  "user": "datadog",
  "pwd": "datadog",
  "roles": [
    { role: "read", db: "admin" },
    { role: "clusterMonitor", db: "admin" },
    { role: "read", db: "local" }
  ]
}

db.createUser(ddUser);

use ddTest

db.metrics.insertOne( { name:"my_metric", value:_rand()*1000 } );

exit
EOF

echo "MongoDB Install Script - v4.4 - Completed"
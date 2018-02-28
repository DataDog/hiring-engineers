#!/bin/bash
# tsn userdata for host

# Update system
yum update -y
logger -p user.notice "BOOTSTRAP: Updating system - $?"

# Installing Docker
yum install -y docker
logger -p user.notice "BOOTSTRAP: Installing Docker - $?"

# Installing Docker Compose
curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
logger -p user.notice "BOOTSTRAP: Installing Docker Compose - $?"

# Starting Docker
/etc/init.d/docker start
logger -p user.notice "BOOTSTRAP: Starting Docker Daemon - $?"

# Writing docker-compose.yml
mkdir -p /tmp/datadog
cat > /tmp/datadog/docker-compose.yml <<EOF
version: "3.4"

volumes:
    mysqldata:

networks:
    frontend: 
    backend:

services:
  dd:
    image: "datadog/docker-dd-agent:latest"
    expose:
    - 8126
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
    - /proc/:/host/proc/:ro
    - /cgroup/:/host/sys/fs/cgroup:ro
    - ./dd-agent/conf.d:/conf.d
    - ./dd-agent/checks.d:/checks.d
    networks:
      backend:
        aliases:
          - dd
    restart: on-failure
    healthcheck:
      test: ["CMD", "nc", "-vvv", "localhost", "8126"]
      interval: 30s
      timeout: 5s
      retries: 2
      start_period: 20s
    env_file:
    - env/dd.env

  mysql:
    image: "mysql"
    expose:
    - 3306
    volumes:
    - mysqldata:/data
    - ./mysql/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d
    networks:
      backend:
        aliases:
        - mysql
    restart: on-failure
    depends_on:
    - dd
    env_file:
    - env/mysql.env

  flask:
    build:
      context: flask-app/
    ports:
    - 80:5000
    networks:
      frontend:
      backend:
        aliases:
        - flask
    restart: on-failure
    depends_on:
    - dd
    env_file:
    - env/flask.env
EOF

logger -p user.notice "BOOTSTRAP: Writing docker-compose.yml - $?"

# Making the directory for flask-app
mkdir -p /tmp/datadog/flask-app
logger -p user.notice "BOOTSTRAP: making flask-app dir - $?"

# Writing the flask-app Dockerfile
cat > /tmp/datadog/flask-app/Dockerfile <<EOF
FROM python:alpine
ARG FLASK_APP
LABEL maintainer="tim.noeding@gmail.com"

RUN mkdir /code && \
    pip install --no-cache-dir flask blinker ddtrace

COPY flask-example.py /code/flask-example.py

WORKDIR /code

CMD nc -z dd 8126; sleep 10; python -m flask run --host=0.0.0.0
EOF

logger -p user.notice "BOOTSTRAP: Writing flask-app Dockerfile - $?"

# Writing flask-app application code
cat > /tmp/datadog/flask-app/flask-example.py <<EOF
from flask import Flask
import logging
import sys
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# setting the datadog agent location
tracer.configure(hostname="dd", port=8126)

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# Trace middleware object
traced_app = TraceMiddleware(app, tracer, service="dd-flask-app", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run()
EOF

logger -p user.notice "BOOTSTRAP: wrote flask-example.py - $?"

# Writing dd-agent dir
mkdir -p /tmp/datadog/dd-agent/checks.d
mkdir -p /tmp/datadog/dd-agent/conf.d
cat > /tmp/datadog/dd-agent/checks.d/my_metric.py <<EOF
# tsn - tech challenge 2018
from checks import AgentCheck
import random
class my_metric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric.my_metric', random.randint(0,1000), tags=['test_tag'])
EOF

cat > /tmp/datadog/dd-agent/conf.d/my_metric.yaml <<EOF
init_config:
        min_collection_interval: 45
instances:
        [{}]
EOF

cat > /tmp/datadog/dd-agent/conf.d/mysql.yaml <<EOF
init_config:

instances:
  - server: mysql
    user: <db_user>
    pass: <db_pass>
    options:
          replication: 0
          galera_cluster: 1
          extra_status_metrics: true
          extra_innodb_metrics: true
          extra_performance_metrics: false
          schema_size_metrics: false
          disable_innodb_metrics: false
    tags:
          - mysql_tag1
          - mysql_tag2
EOF

# Writing env directory and files
mkdir -p /tmp/datadog/env
cat > /tmp/datadog/env/dd.env <<EOF
API_KEY=<dd_api_key>
SD_BACKEND=docker
DD_APM_ENABLED=true
DD_PROCESS_AGENT_ENABLED=true
TAGS=test_tag_1,test-key-1:test-value-1
EOF

cat > /tmp/datadog/env/flask.env <<EOF
FLASK_APP=flask-example.py
EOF

cat > /tmp/datadog/env/mysql.env <<EOF
MYSQL_ROOT_PASSWORD=<mysql_root_pass>
MYSQL_DATABASE=<db_name>
EOF

# Writing mysql directory and files
mkdir -p /tmp/datadog/mysql/docker-entrypoint-initdb.d
cat > /tmp/datadog/mysql/docker-entrypoint-initdb.d/perms.sql <<EOF
use mysql;
CREATE USER '<db_user>'@'%' IDENTIFIED BY '<db_pass>';
GRANT REPLICATION CLIENT ON *.* TO '<db_user>'@'%' WITH MAX_USER_CONNECTIONS 5;
GRANT PROCESS on *.* TO '<db_user>'@'%';
use performance_schema;
GRANT SELECT ON performance_schema.* TO '<db_user>'@'%';
flush privileges;
EOF

logger -p user.notice "BOOTSTRAP: Application env and mysql configured - $?"

# Run applications
sleep 60
cd /tmp/datadog
screen -d -m /usr/local/bin/docker-compose --project-directory /tmp/datadog/ up
logger -p user.notice "BOOTSTRAP: Application Started"
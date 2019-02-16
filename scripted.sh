#!/usr/bin/env bash
# Setup the lab, and create answers MD
BASEDIR="$(dirname $0)"

docit() {
        echo "$@" >> answers.md
}

bootstrap() {
## bootstrap
# this is the bootstrap for this, before cloneing the forked repo run this
# store your API and Keys in .env, this is required...
# for exampe
# All my secrets
# export DB_PASS="DBPASS"
# export DD_API_KEY='DDAPIKEY"
# export DD_APP_KEY='DDAPPKEY"
sudo apt install git curl docker.io  -y
sudo systemctl start docker
git clone https://github.com/edennuriel/hiring-engineers.git
cd hiring-engineers
#####
}

docit '#PREPARING'
docit ' - lab environment - install curl and git, get the repo and install the agentr'

bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
docit '#METRICS'
docit ' - add tags to the agent config and restart the agent'

# Adding Custom tags to agent and restarting agent
echo << EOF >> /etc/datadog-agent/datadog.yaml

#custom tags
tags:
  class:physical
  env:lab
  role:scratchpad
  role:scratchpad
EOF

systemctl restart datadog-agent
docit ' - URL showing the tags as variables and used in group by viz of host map is here: docit "https://p.datadoghq.com/sb/q6rr0gs671wrdhi2-f115cbc602039fff6de4388bd9161064"'
docit ' - static image'

docit " - Install mysql on the host + mongo as docker container"

sudo apt-get install mysql-server
[[ $(sudo docker ps -a | grep mongo) ]] || sudo docker run -d --name mongo mongo:latest

docit ' - Configure mysql integration create db user, grants'
mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '$DB_PASS';"
mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

mysql -u datadog --password="$DB_PASS" -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"

##mysql -u datadog --password="$DB_PASS" -e "show slave status" && \
#echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
#echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"

mysql -u datadog --password="$DB_PASS" -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
echo -e "\033[0;31mMissing PROCESS grant\033[0m"

mysql -u datadog --password="$DB_PASS" -e "SELECT * FROM performance_schema.threads" && \
echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
echo -e "\033[0;31mMissing SELECT grant\033[0m"

docit " - Update dd agent conf for mysql check with user/pass endpoint and tags"
cat << EOF > /etc/datadog-agent/conf.d/mysql.yaml

init_config:

instances:
  - server: localhost
    user: datadog
    pass: $DB_PASS
    tags:
        - mysql5.7
        - tempdb
    options:
      replication: 0
      galera_cluster: 1
EOF

docit " - Restart agent and check that the check is running"
systemctl restart datadog-agent 
datadog-agent status | grep mysql

docit ' - Configure custom metric check and metric'
docit ' - Use python script () to update a gauge type with random int, place it with check scripts and create metric conf with min update interval set to 45 seconds'
grep -v "#" my_metric.py > /etc/datadog-agent/checks.d/my_metric.py

echo  << EOF > /etc/datadog-agent/conf.d/my_metric.yaml
init_config:

instances:
  - min_collection_interval: 45
EOF

docit " - restart agent and run check for my_metric"
docit '"Bonus Question Can you change the collection interval without modifying the Python check file you created?"...'
docit "...Yes, Check interval is controled by the metric conf not the check code. by changinh the conf we control the reporting frequency"

docit "#VISUALIZING"
docit " - I used tth web UI to create the graphs, then the get_boards to extract the configuration of the graphs so i can create it via the rest api"
docit " - It seems the python API does not have Dashboard method as documented in the API section of the docit <url>, insteat a Timetable API was available (also swapped widgets list for graphs) so maybe some docit updates is due or maybe I was missing something"
docit " - get_boards is hard coded for the board i created as the template <> create board script is here <>"
docit " - link to the vizualisation https://app.datadoghq.com/account/settings#a23c56f6c31444f2a2e1815f71756bddce8a2fff60474752c69f8b91d4ddf096"
docit " - and a local image too"
docit 'Bonus Question: What is the Anomaly graph displaying?... It uses the selected algorithm to paint in red a pattern that is considered outside of the normal behavior of the metric by comparing it to the metric history'
docit 'PS:  to get some performence figures on the mysql.performence.opentables I'm just running a select all on all tables on all databases for a 100 times or so, that will be an anomoly for sure"
for d in $(mysql -e "show databases"); do for t in $(mysql -e "show tables" -D $d -N -s -r); do mysql -D $d -N -s -r -e "select * from $t" ; done ;done >/dev/null 2>&1

docit "#MONITORING"
docit " - configured monitor for my_metric via UI and configure scheduled downtime"
docit " - scripted the creation of the monitor here "
docit " - for the scheduled downtime, i used to scheduled (friday 7am - Mon 9am and Mon,Tue,Wed,Thur 7pm-9am) I could'nt grasp why the schedular makes it hard to pick any time or why there's no cron syntax available, also the time UI is iffy with keyboard controls"
docit " - here is an example of a notification for the scheduled downtime "
docit " - and for the monitor triggering "

docit "#APMING"
docit " - configure agent conf to enable APM" 
#configuering APM
echo apm_config: >>  /etc/datadog-agent/datadog.yaml
echo   enabled: true >>  /etc/datadog-agent/datadog.yaml
echo "  env:lab" >>  /etc/datadog-agent/datadog.yaml

docit " - preping for flask, using conda all as root...(install conda, create env, install flask, add app, create .flaskenv, pip dd drace and flaskenv"
[[ $(command -v conda) ]] || sudo curl -O https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
[[ $(command -v conda) ]] || bash Anaconda3-2018.12-Linux-x86_64.sh -b
[[ $(command -v conda) ]] || sudo ln -s /root/anaconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh
[[ $(command -v conda) ]] || source /etc/profile.d/conda.sh
[[ $(conda info --env | grep flaskenv) ]]  || conda create -n flaskenv
conda activate flaskenv
conda install flask
pip install ddtrace datadog python-dotenv
echo << EOF >> .flaskenv
FLASK_APP=app.py
FLASK_RUN_PORT=5050
SERVER_NAME="0.0.0.0:5050"
EOF

docit " - run the app with ddtrace and generate some traffic"
ddtrace-run flask run --host 0.0.0.0 &
for i in {1..100}; do for ep in $(grep -Po "route\(\K([^\)]+)" app.py | sed "s/'//g"); do curl http://localhost:5050$ep; done ;curl http://localhost:5050/$i ; done
docit " - chart "
docit 'Bonus Question: What is the difference between a Service and a Resource?... service is an endpoint you access to get service, like db, web server, resource is more granular rest endpoint, db table, specific query or file'

docit "#LOGGING"
docit " - configured rsyslog to forward events from auth.log and use TLS'
echo << EOF > /etc/rsyslog.d/datadog.conf 
$template DatadogFormat,"8e85933353733f92da0bd91b0f1c837a <%pri%>%protocol-version% %timestamp:::date-rfc3339% %HOSTNAME% %app-name% - - - %msg%\n"

ruleset(name="infiles") {
    action(type="omfwd" target="intake.logs.datadoghq.com" protocol="tcp" port="10514" template="DatadogFormat")
}
EOF

echo <<EOF >> /etc/rsyslog.d/datadog.conf
# kernel log example...	
input(type="imfile" ruleset="infiles" Tag="kernal" File="/var/log/datadog/kernel.log" StateFile="/var/log/datadog/kernel.id")
EOF


}

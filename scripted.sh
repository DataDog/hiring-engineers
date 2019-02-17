#!/usr/bin/env bash
# Setup the lab, and create answers MD
BASEDIR="$(dirname $0)"

docit() {
        echo "$@"
        echo "$@" >> answers.md
}

bootstrap(){
# this is happenning before the git clone
# make sure the host is ready
# prms
# All my secrets
# keep .env file with the following:
# export DB_PASS="somedbpassowrd"
# export DD_API_KEY='DD api key"
# export DD_APP_KEY='dd app key"
# this is mandatory for this to work
source .env
sudo apt install git curl docker.io  -y > /dev/null 2>&1
sudo systemctl start docker
git clone https://github.com/edennuriel/hiring-engineers.git
cd hiring-engineers
}
source resources

docit '# PREPARING'
docit ' - lab environment - install curl, get the repo and install the agent'

[[ command -v datadog-agent ]] || bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
docit '# METRICS'
docit ' - add tags to the agent config and restart the agent'

# Adding Custom tags to agent and restarting agent
cat << EOF >> /etc/datadog-agent/datadog.yaml

#custom tags
tags:
  class:physical
  env:lab
  role:scratchpad
  role:scratchpad
EOF

systemctl restart datadog-agent
docit ' - URL showing the tags as variables and used in group by viz of host map is [here] (https://p.datadoghq.com/sb/q6rr0gs671wrdhi2-f115cbc602039fff6de4388bd9161064)'
docit ' - or in the host map screenshot here'
docit '![static_image](https://github.com/edennuriel/hiring-engineers/blob/master/screenshots/tags-added.png)'

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
echo "waiting for mysql check"
sleep 2
while [[ ! $(datadog-agent status | grep mysql) ]]; do echo -n "."; sleep 1; done

docit ' - Configure custom metric check and metric'
docit ' - Use python script [my_metric.py] (https://github.com/edennuriel/hiring-engineers/blob/master/my_metric.py) to update a gauge type with random int, place it with check scripts and create metric conf with min update interval set to 45 seconds'
grep -v "#" my_metric.py > /etc/datadog-agent/checks.d/my_metric.py

echo  << EOF > /etc/datadog-agent/conf.d/my_metric.yaml
init_config:

instances:
  - min_collection_interval: 45
EOF

docit " - restart agent and run check for my_metric"
docit '"Bonus Question Can you change the collection interval without modifying the Python check file you created?"...'
docit "...Yes, Check interval is controled by the metric conf not the check code. by changinh the conf we control the reporting frequency"

docit '# VISUALIZING'
docit ' - I used tth web UI to create the graphs, then the get_boards to extract the configuration of the graphs so i can create it via the rest api'
docit ' - It seems the python API does not have Dashboard method as documented in the API section of the [doc] (https://docs.datadoghq.com/api/?lang=python#create-a-dashboard), insteat a Timetable API was available (also swapped widgets list for graphs) so maybe some docit updates is due or maybe I was missing something'
docit ' - get_boards is hard coded for the board I created in the UI, create board script is here [create_board](https://github.com/edennuriel/hiring-engineers/blob/master/create_board.py)'
docit ' - link to [graph] (https://app.datadoghq.com/graph/embed?token=a23c56f6c31444f2a2e1815f71756bddce8a2fff60474752c69f8b91d4ddf096)'
docit '![static image](https://github.com/edennuriel/hiring-engineers/blob/master/screenshots/dashboard.png) '
docit 'Bonus Question: What is the Anomaly graph displaying?... It uses the selected algorithm to paint in red a pattern that is considered outside of the normal behavior of the metric by comparing it to the metric history'
docit 'PS:  to get some performence figures on the mysql.performence.opentables Im just running a select all on all tables on all databases for a 100 times or so, that will be an anomoly for sure'

query_all_tables() {
	for d in $(mysql -e "show databases"); do for t in $(mysql -e "show tables" -D $d -N -s -r); do mysql -D $d -N -s -r -e "select * from $t" ; done ;done >/dev/null 2>&1
}

query_all_tables

docit "# MONITORING"
docit " - configured monitor for my_metric via UI and configure scheduled downtime"
docit " - scripted the creation of the monitor here "
docit " - for the scheduled downtime, i used to scheduled (friday 7am - Mon 9am and Mon,Tue,Wed,Thur 7pm-9am) I could'nt grasp why the schedular makes it hard to pick any time or why there's no cron syntax available, also the time UI is iffy with keyboard controls"
docit " - here is an example of a notification for the scheduled downtime"
docit '![email](https://github.com/edennuriel/hiring-engineers/blob/master/screenshots/downtime-email.png)'

docit "# APMING"
docit " - configure agent conf to enable APM" 
#configuering APM
echo apm_config: >>  /etc/datadog-agent/datadog.yaml
echo   enabled: true >>  /etc/datadog-agent/datadog.yaml
echo "  env:lab" >>  /etc/datadog-agent/datadog.yaml

docit " - preping for flask, using conda all as root...(install conda, create env, install flask, add app, create .flaskenv, pip dd drace and flaskenv"
# for the life of me, don't know why subshell does not see conda... probably where the intilization happens... echo testing if conda is there "$(command -v conda)"
need_conda_install() {
        rm /tmp/conda >/dev/null 2>&1
        command -v conda > /tmp/conda
        if [[ -f /tmp/conda ]]
        then
                echo no
        else
                echo yes
        fi
}

if [[ need_conda_install == yes ]]
then
        echo installing conda
        sudo curl -O https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh
        sudo bash Anaconda3-2018.12-Linux-x86_64.sh -b
        sudo ln -s /root/anaconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh
fi

source /etc/profile.d/conda.sh
#just try to create will fail if already exist
conda create -n flaskenv >/dev/null 2>&1
conda activate flaskenv
conda install flask
pip install ddtrace datadog python-dotenv
touch .flaskenv
cat << EOF >> .flaskenv
FLASK_APP=app.py
FLASK_RUN_PORT=5050
SERVER_NAME="0.0.0.0:5050"
EOF

docit " - run the app with ddtrace in the background and generate some traffic"
ddtrace-run flask run --host 0.0.0.0 & >/dev/null 2>&1
for i in {1..100}; do for ep in $(grep -Po "route\(\K([^\)]+)" app.py | sed "s/'//g"); do curl http://localhost:5050$ep; done ;curl http://localhost:5050/$i ; done >/dev/null 2>&1
docit " - chart "
docit 'Bonus Question: What is the difference between a Service and a Resource?... service is an endpoint you access to get service, like db, web server, resource is more granular rest endpoint, db table, specific query or file'

docit "# LOGGING"

docit ' - configured rsyslog to forward events from auth.log and use TLS'
if [[ $(grep "$DD_API_KEY" /etc/rsyslog.d/datadog.conf) ]]
then
	echo already rsyslog.d is already configured for dd
else
	echo << EOF > /etc/rsyslog.d/datadog.conf 
# files
# auth for exampe
input(type="imfile" ruleset="infiles" Tag="auth" File="/var/log/auth.log" StateFile="/var/log/auth.state")
$template DatadogFormat,"$DD_API_KEY <%pri%>%protocol-version% %timestamp:::date-rfc3339% %HOSTNAME% %app-name% - - - %msg%\n"

ruleset(name="infiles") {
    action(type="omfwd" target="intake.logs.datadoghq.com" protocol="tcp" port="10514" template="DatadogFormat")
}

$DefaultNetstreamDriverCAFile /etc/ssl/certs/intake.logs.datadoghq.com.crt
$ActionSendStreamDriver gtls
$ActionSendStreamDriverMode 1
$ActionSendStreamDriverAuthMode x509/name
$ActionSendStreamDriverPermittedPeer *.logs.datadoghq.com
*.* @@intake.logs.datadoghq.com:10516;DatadogFormat
EOF

fi

# need some work here to look for it and add it, for now just add
echo 'module(load=imfile PollingInterval=10)' >> /etc/rsyslog.conf

# get cert 
curl -O https://docs.datadoghq.com/crt/intake.logs.datadoghq.com.crt
mv intake.logs.datadoghq.com.crt /etc/ssl/certs/


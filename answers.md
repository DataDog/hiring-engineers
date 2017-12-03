# ANSWERS

## Prerequisites - Setup the environment
Here are the steps I took to install docker and the Datadog agent on Ubuntu 12.04 VM:

[Per Getting Started with Vagrant](https://www.vagrantup.com/intro/getting-started/index.html)
- [Install and run VirtualBox](https://www.virtualbox.org/)
- [Install the lastest version of Vagrant](https://www.vagrantup.com/downloads.html)

### Vagrant setup
- In the terminal, navigate to a folder you wish to work from
- Create the Vagrantfle
```
vagrant init hashicorp/precise64
```
- Start the virtual machine
```
vagrant up
```
- Enter the virtual machine
```
vagrant ssh
```

### Docker install on vagrant@precise64
- Install curl
```
sudo apt-get install curl
```

- Install docker with shell script
```
curl -L https://gist.github.com/steakknife/9094991/raw/run_me_001__install_docker_and_fixes.sh | bash
```

### Datadog agent install
- Use the one-step install line at https://app.datadoghq.com/account/settings#agent/docker
- Append ``sudo`` to the front

### Start the docker container with the Datadog agent
- In one terminal tab start the docker daemon:
```
sudo docker daemon
```
- In a separate terminal tab start the dd-agent container:
```
sudo docker start dd-agent
```

### Verification of docker and dd-agent install
```
docker --version
sudo docker ps
```
![Screenshot](/screenshots/01_dd-agent_installed.png?raw=true "Install Verification")

## COLLECTING METRICS:

## Add Tags:
- Tags added to the datadog.conf file:<br/>
![Screenshot](/screenshots/02_datadog.conf.png?raw=true "datadog.conf")

- Host Map page in Datadog:<br/>
![Screenshot](/screenshots/02_host_map_page.png?raw=true "Host Map page")

## Install and link a database:
- Postgres installed on VM:<br/>
![Screenshot](/screenshots/03_postgres_installed.png?raw=true "Postgre installed")

- Postgres integration connected:<br/>
![Screenshot](/screenshots/03_postgres_integration.png?raw=true "Postgre integration")

## Custom Agent Check:
- conf.d/my_metric.yaml and checks.d/my\_metric.yaml:<br/>
![Screenshot](/screenshots/04_yaml_py_files.png?raw=true "yaml and py files")

- my_metric shown in the metric explorer:<br/>
![Screenshot](/screenshots/04_metric_explorer.png?raw=true "yaml and py files")

## Change Custom Agent Check Interval:
- Changed via conf.d/my_metric.yaml<br/>
![Screenshot](/screenshots/05_yaml_file.png?raw=true "yaml file")

- my_metric shown in the metric explorer:<br/>
![Screenshot](/screenshots/05_metric_explorer.png?raw=true "yaml and py files")

## VISUALIZING DATA:

## Create a Timeboard:
![Screenshot](/screenshots/06_TimeBoard.png?raw=true "TimeBoard")

## Timeboard over 5 minutes:
- Timeboard<br/>
![Screenshot](/screenshots/07_TimeBoard.png?raw=true "TimeBoard")

- Taking a snapshot of a graph on the TimeBoard<br/>
![Screenshot](/screenshots/07_TakeSnapshot.png?raw=true "Snapshot")

- Snapshot received<br/>
![Screenshot](/screenshots/07_SnapshotReceived.png?raw=true "Snapshot")

- Bonus Question<br/>
The anomaly graph is displaying a shaded gray area which represents the area the metric is expected to be in.  The blue line represents the actual metric.  The red points indicate outliers.

## MONITORING DATA:

## Create a Monitor:
- Define the metric<br/>
![Screenshot](/screenshots/08_DefineMetric.png?raw=true "Define Metric")

- Set alert conditions<br/>
![Screenshot](/screenshots/08_SetAlertConditions.png?raw=true "Set alert conditions")

- Monitor message<br/>
![Screenshot](/screenshots/08_MonitorMessage.png?raw=true "Monitor message")

- Email notification<br/>
![Screenshot](/screenshots/08_EmailNotification.png?raw=true "Email notification")

## Downtime:
- Downtime on week nights from 7pm to 9am<br/>
![Screenshot](/screenshots/09_DowntimeNights.png?raw=true "Downtime")

- Downtime on Weekends<br/>
![Screenshot](/screenshots/09_DowntimeWeekends.png?raw=true "Downtime")

## COLLECTING APM DATA:

- Link to Dashboard: https://app.datadoghq.com/dash/411155/apm-dashboard

- Screenshot of Dashboard<br/>
![Screenshot](/screenshots/10_APMDashboard.png?raw=true "APM Dashboard")

- A service is a set of processes that work together to serve up an application.  A resource is a particular query to a service. - Reference: https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-

## FINAL QUESTION:

## Use for Datadog

- I'm not sure if this is a 'Creative' use of datadog, but I wish I could of used it when I worked for EY.  I ran a project that used servers to run a program called Captiva.  Captiva performed OCR (optical character recognition) to read data from PDF tax return files.  My project was heavily used close to the tax return deadline and I had to manually monitor the servers and services to make sure nothing went offline.

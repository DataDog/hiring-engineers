Your answers to the questions go here.

### Level 0 (optional) - Setup an Ubuntu VM

I Amazon EC2 to create Ubuntu environment.

The machine image I used is `Ubuntu Server 16.04 LTS (HVM), SSD Volume Type` and its ID is `ami-6e1a0117`.

```
## Using AWS CLI
$ aws --version
aws-cli/1.11.155 Python/2.7.12 Darwin/16.7.0 botocore/1.7.13

## Create an instance
$ aws ec2 run-instances --image-id ami-6e1a0117 --instance-type t2.micro --key-name dd-challenge
{
    "Instances": [
        {
...
            "InstanceId": "i-0be3d85889b8b029d",
...
            "NetworkInterfaces": [
                {
...
                    "Groups": [
                        {
                            "GroupName": "default",
                            "GroupId": "sg-08897867"
...

## Adding an ingress rule to the security group to connect with SSH
$ aws ec2 authorize-security-group-ingress --group-id sg-08897867 --cidr $(curl -s checkip.amazonaws.com)/32 --protocol tcp --port 22

## Getting public hostname to connect
$ aws ec2 describe-instances --instance-id i-0be3d85889b8b029d
{
    "Reservations": [
        {
            "Instances": [
                {
...
                    "PublicDnsName": "ec2-52-34-99-226.us-west-2.compute.amazonaws.com",
...

## Avoid `UNPROTECTED PRIVATE KEY FILE` error
$ chmod 600 ~/Downloads/dd-challenge.pem

## Connect to the instance
$ ssh -i ~/Downloads/dd-challenge.pem ubuntu@ec2-52-34-99-226.us-west-2.compute.amazonaws.com
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-1022-aws x86_64)

...

ubuntu@ip-172-31-22-56:~$
```

### Level 1 - Collecting your Data

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.

```
## Install Datadog Agent
$ DD_API_KEY=<<hidden because it's a secret information>> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
...
Waiting for metrics.................................

Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.

If you ever want to stop the Agent, run:

    sudo /etc/init.d/datadog-agent stop

And to run it again run:

    sudo /etc/init.d/datadog-agent start

## Confirm it is properly running
$ sudo systemctl status dd-agent
● dd-agent.service
   Loaded: not-found (Reason: No such file or directory)
   Active: inactive (dead)
ubuntu@ip-172-31-22-56:~$ sudo systemctl status datadog-agent
● datadog-agent.service - "Datadog Agent"
   Loaded: loaded (/lib/systemd/system/datadog-agent.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2017-09-19 09:05:09 UTC; 1min 59s ago
  Process: 12276 ExecStart=/opt/datadog-agent/bin/start_agent.sh (code=exited, status=0/SUCCESS)
 Main PID: 12281 (supervisord)
    Tasks: 12
   Memory: 130.5M
      CPU: 4.008s
   CGroup: /system.slice/datadog-agent.service
           ├─12281 /opt/datadog-agent/embedded/bin/python /opt/datadog-agent/bin/supervisord -c /etc/dd-agent/supervisor.conf
           ├─12285 /opt/datadog-agent/bin/trace-agent
           ├─12286 /opt/datadog-agent/embedded/bin/python /opt/datadog-agent/agent/ddagent.py
           ├─12287 /opt/datadog-agent/embedded/bin/python /opt/datadog-agent/agent/dogstatsd.py --use-local-forwarder
           ├─12294 /opt/datadog-agent/embedded/bin/python /opt/datadog-agent/agent/agent.py foreground --use-local-forwarder
           └─12640 mpstat 1 3

Sep 19 09:06:12 ip-172-31-22-56 dd.dogstatsd[12287]: INFO (dogstatsd.py:274): Flush #6: flushed 2 metrics, 0 events, and 0 service check runs
Sep 19 09:06:15 ip-172-31-22-56 dd.forwarder[12286]: INFO (transaction.py:177): Flushing 1 transaction during flush #20
Sep 19 09:06:15 ip-172-31-22-56 dd.collector[12294]: INFO (collector.py:530): Finished run #4. Collection time: 4.15s. Emit time: 0.01s
Sep 19 09:06:22 ip-172-31-22-56 dd.dogstatsd[12287]: INFO (dogstatsd.py:274): Flush #7: flushed 10 metrics, 0 events, and 0 service check runs
Sep 19 09:06:32 ip-172-31-22-56 dd.dogstatsd[12287]: INFO (dogstatsd.py:274): Flush #8: flushed 10 metrics, 0 events, and 0 service check runs
Sep 19 09:06:34 ip-172-31-22-56 dd.collector[12294]: INFO (collector.py:530): Finished run #5. Collection time: 4.1s. Emit time: 0.01s
Sep 19 09:06:34 ip-172-31-22-56 dd.collector[12294]: INFO (collector.py:533): First flushes done, next flushes will be logged every 10 flushes.
Sep 19 09:06:42 ip-172-31-22-56 dd.dogstatsd[12287]: INFO (dogstatsd.py:274): Flush #9: flushed 10 metrics, 0 events, and 0 service check runs
Sep 19 09:06:52 ip-172-31-22-56 dd.dogstatsd[12287]: INFO (dogstatsd.py:274): Flush #10: flushed 10 metrics, 0 events, and 0 service check runs
Sep 19 09:06:52 ip-172-31-22-56 dd.dogstatsd[12287]: INFO (dogstatsd.py:276): First flushes done, 5 flushes will be logged every 70 flushes.
```

* Bonus question: In your own words, what is the Agent?

The agent is a daemonized process that collects system and application metrics from the server to Datadog's API.

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

```
## Add tag definition to the agent config file
$ sudo vim /etc/dd-agent/datadog.conf
## added `tags: y13i, role:test`

## Restart the agent to apply the setting
$ sudo systemctl restart datadog-agent
```

![Host Map](images/level1-1.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose MongoDB so I followed the instruction [Install MongoDB Community Edition on Ubuntu — MongoDB Manual 3.4](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

Install MongoDB.

```
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
$ echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
```

Start MongoDB and confirm it is running.

```
$ sudo systemctl start mongod
$ sudo systemctl status mongod
● mongod.service - High-performance, schema-free document-oriented database
   Loaded: loaded (/lib/systemd/system/mongod.service; disabled; vendor preset: enabled)
   Active: active (running) since Tue 2017-09-19 09:38:57 UTC; 51s ago
     Docs: https://docs.mongodb.org/manual
 Main PID: 18024 (mongod)
    Tasks: 20
   Memory: 58.7M
      CPU: 241ms
   CGroup: /system.slice/mongod.service
           └─18024 /usr/bin/mongod --config /etc/mongod.conf

Sep 19 09:38:57 ip-172-31-22-56 systemd[1]: Started High-performance, schema-free document-oriented database.
$ tail -5 /var/log/mongodb/mongod.log
2017-09-19T09:38:57.686+0000 I INDEX    [initandlisten] build index on: admin.system.version properties: { v: 2, key: { version: 1 }, name: "incompatible_with_version_32", ns: "admin.system.version" }
2017-09-19T09:38:57.686+0000 I INDEX    [initandlisten] 	 building index using bulk method; build may temporarily use up to 500 megabytes of RAM
2017-09-19T09:38:57.687+0000 I INDEX    [initandlisten] build index done.  scanned 0 total records. 0 secs
2017-09-19T09:38:57.687+0000 I COMMAND  [initandlisten] setting featureCompatibilityVersion to 3.4
2017-09-19T09:38:57.687+0000 I NETWORK  [thread1] waiting for connections on port 27017
```

Install [Datadog's MongoDB integration](https://app.datadoghq.com/account/settings#integrations/mongodb).

```
## Start mongo shell
$ mongo
>

// Create user for monitoring: datadog
> db.createUser({"user":"datadog", "pwd": "****hidden****", "roles" : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})
Successfully added user: {
	"user" : "datadog",
	"roles" : [
		{
			"role" : "read",
			"db" : "admin"
		},
		{
			"role" : "clusterMonitor",
			"db" : "admin"
		},
		{
			"role" : "read",
			"db" : "local"
		}
	]
}
> ^C
bye

## Confirm it is properly created
$ echo "db.auth('datadog', '****hidden****')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" &&
> echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"
datadog user - OK

## Create integration config file
$ sudo vim /etc/dd-agent/conf.d/mongo.yaml
$ cat /etc/dd-agent/conf.d/mongo.yaml
init_config:

instances:
- server: mongodb://datadog:****hidden****@localhost:27017
  tags:
  - y13i
  - role:db
  - role:mongod
```

Check the data collected with the integration.

![Host Map - MongoDB integration](images/level1-2.png)

![MongoDB dashboard](images/level1-3.png)

* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

Custom metrics can be collected via DogStatsD. ([Sending Metrics with DogStatsD](https://docs.datadoghq.com/guides/metrics/))

I created Ruby script to produce and send random values.

Install Ruby and DogStatsD library.

```
$ apt install -y ruby
$ ruby --version
ruby 2.3.1p112 (2016-04-26) [x86_64-linux-gnu]
$ sudo gem install dogstatsd-ruby
```

The actual script is this. It produces random value between 0 to 1 and sends to DogStatsD every 5 seconds.

```ruby:random.rb
require "datadog/statsd"

statsd = Datadog::Statsd.new

loop do
  value = rand()
  puts value
  statsd.histogram("test.support.random", value)

  sleep 5
end
```

Run the script and confirm results on Host Map.

```
$ ruby random.rb
0.7408150575386946
0.20310512932428793
0.8149465133771042
0.26299169033404113
0.47150568841674567
0.9643894862551654
0.7237233890096653
...
```

![Random metric](images/level1-4.png)

Since `histogram` method of statsd is used, `avg`, `count`, `max`, `median` and `95percentile` are automatically calculated.

### Level 2 - Visualizing your Data

* Since your database integration is reporting now, clone your database integration dashboard and add additional database metrics to it as well as your `test.support.random` metric from the custom Agent check.

At the first, clone MongoDB dashboard.

![Clone MongoDB dashboard](images/level2-1.png)

I added graph and value display for MongoDB insert ops count and random metric that I created in the last section.

Then I issued some insert commands to my MongoDB repeatedly by my hand.

```
$ mongo --eval 'db.myCollection.insert([{value: 123}])' test
```

![Customized dashboard](images/level2-2.png)

* Bonus question: What is the difference between a timeboard and a screenboard?

I think that the biggest difference between a timeboard and a screenboard is freedom of customization.

A timeboard mainly focus on graphs, so it is auto layouted, easy to create, good at monitoring each service components' metrics.

A screenboard offeres more customizability such as free layout and more various items than timeboard. It is very good choice for creating dashboard visualizing entire service informations.

* Take a snapshot of your `test.support.random` graph and draw a box around a section that shows it going above 0.90. Make sure this snapshot is sent to your email by using the @notification

I added an comment on graph in Metrics Explorer.

Additionally I used notebook feature to add constant 0.90 line.

[Link to the Notebook](https://app.datadoghq.com/notebook/15050/Yoriki%2019%20Sep%202017%2021%3A51)

![Snapshot](images/level2-3.png)

### Level 3 - Alerting on your Data

* Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes

I created a [monitor](https://app.datadoghq.com/monitors#2856163?group=all&live=4h) for detecting high metric value within `test.support.random.max`.

![Monitor](images/level3-1.png)

* Bonus points:  Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up.

Defining metric `from` parameter `role:test` means **collect data from all hosts tagged with role:test**. When I scale out the infrastructure I need to tag new hosts as `role:test` in order to assign this monitor.

![from](images/level3-2.png)

* Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message).  Make sure that the monitor will notify you via email.
* This monitor should alert you within 15 minutes. So when it does, take a screenshot of the email that it sends you.

I received monitor alert email below.

![Email](images/level3-2.png)

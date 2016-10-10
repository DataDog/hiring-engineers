# Level (-1) - Hello, world!

**[TODO]**

[my Linkedin](https://www.linkedin.com/in/samxjacobs).

Hi there! 

# Level 0 - Setting up Ubuntu

To ensure that we won't run into any OS or dependency issues, we'll start by creating a new virtual machine running Ubuntu. After installing VirtualBox and Vagrant, this can be done with the command

```
$ vagrant init hashicorp/precise64
```

This adds a new Vagrantfile to the project directory. Because we'll be editing the Datadog Agent config files on the vm to complete these challenges, it will be desirable to replicate those changes in the project directory so they can be pushed to the repo for submission.

Conveniently, Vagrant has the ability to sync folders between the vm and the host. To set this up, we only need to add the following line to our Vagrantfile:

```
config.vm.synced_folder "dd-agent/", "/etc/dd-agent", create: true, mount_options: ["dmode=775, fmode=664"]
```

The "create" option here will create the directory "dd-agent" in the project directory, and the "mount_options" are set to enable the Datadog Agent to write logs to the directory within the vm (NOTE: it is not advisable to give global write priveleges in general, but in the case of running dev on my laptop I think we're pretty ok).

Once we've done this, we can spin up our vm and SSH in to begin playing around:

```
$ vargant up
$ vagrant ssh
```

# Level 1 - Collecting our data

## Getting the Agent reporting on our local machine

Installing and activating the Datadog agent is simple enough, using the script provided for your OS of choice (in this case, found at https://app.datadoghq.com/account/settings#agent/ubuntu). After installing **curl**, which isn't by default on our bare bones ubuntu box, the script can be downloaded and run using the following command:

```
vagrant$ DD_API_KEY=<YOUR API KEY>
vagrant$ bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```

We can see that the host is up and reporting metrics in Datadog on the infrastructure list (https://app.datadoghq.com/infrastructure)

![Agent reporting for duty](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/Agent_up_and_running.png?raw=true)


## Bonus Question: What is the Agent?

The Data dog agent is a program that is installed on any server that you want metrics from. It has three main functions: 

* To collect metrics form the system directly and from applications (via integrations)
* To aggregate and summarize those metrics in order to facilitate meaningful monitoring and graphing
* To push those aggregations across the network to Datadog, where they can be viewed in the context of your entire infrastructure

## Adding tags

Tags are user-created, nominal dimensions that make it easier to group and filter hosts within an infrastructure. There are a few sorts of tags, but for now let's restrict ourselves to Agent tags. We'll tag our agent by adding the following line to the agent config file, found (on linux) at /etc/dd-agent/datadog.conf:

```
tags: firstname:sam, lastname:jacobs, hello:world
```

Tags are often structured as key/value pairs, but this is not a requirement. After we've altered the config, we must update the agent by running

```
vagrant$ sudo /etc/init.d/datadog-agent restart
```

We can now see these chages reflected in the Datadog UI on the Host Map (https://app.datadoghq.com/infrastructure/map)

![Agent reporting for duty](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/Tags.png?raw=true)

More info on tags can be found [here](http://docs.datadoghq.com/guides/tagging/).

## Database Integrations

While it's cool that we've been able to get Datadog communicating with a remote host, what we'd really like to do is a) run useful applications on our hosts and b) use Datadog to monitor them. To try this out, let's set up a Postgres database and pull some metrics on it. We'll follow [this guide](http://tecadmin.net/install-postgresql-server-on-ubuntu/) to set up the our DB and [this one](http://docs.datadoghq.com/integrations/postgresql/) to enable Datadog integrations.

The following commands will install Postgres, switch to a DB admin role, and create a Datadog user with the appropriate permissions:

```
vagrant$ sudo apt-get install postgresql postgresql-contrib
vagrant$ sudo su - postgres
postgres$ psql
    create user datadog with password 'helloworld';
    grant SELECT ON pg_stat_database to datadog;
    \q
postgres$ su - vagrant
```

After we've finished on the Postgres side, we still need to add an integration yaml file to Datadog. Because we don't have any special configuration needs, we can use the pre-built yaml.example:

```
vagrant$ sudo cp /etc/dd-agent/conf.d/postgres.yaml.example /etc/dd-agent/conf.d/postgres.yaml
vagrant$ sudo /etc/init.d/datadog-agent restart
```

And in the Host Map we can see our new app on precise64!

![Agent reporting for duty](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/Postgres_Activated.png?raw=true)

## Agent checks

Agent checks are a powerful interface for creating custom metrics and aggregations. They are composed of two parts: the check (a python script that performs calculations and reports metrics), and a config file (that determines how the check will be run and on what instances it will be run). These must be named with the same basename and must be stored in dd-agent/checks.d and dd-agent/conf.d, respectively.

For a quick example, let's write a simple Agent Check that samples a random float between 0.0 and 1.0 every 15 seconds. The code can be found here for the [check file](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/dd-agent/checks.d/random.py) and the [check configuration](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/dd-agent/conf.d/random.yaml). We'll use this check in the following sections for graphing and monitoring.

# Visualizing our data

## Adding the Agent Check to the Database Dashboard

The Agent check that we wrote in teh alst section should be sampling and sending results every 15 seconds

## Bonus: What is the difference between a timeboard and a screenboard?

## Snapshots and Event Notifications

![Event stream notification](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/snapshots_with_at_notification.png?raw=true)

# Alerting on our data

## Setting up the monitor

## Bonus: Multi-alerts!

![Set it as a multi alert](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/multi_alert_setting.png?raw=true)

## Monitor Message and Email notification

![Alert email notification](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/aler_triggered.png?raw=true)

## Bonus: Scheduling Downtime

![Make it repeat](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/downtime_repeating.png?raw=true))

![Send an email notification](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/downtime_notification.png?raw=true)



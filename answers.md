# Level (-1) - Hello, world!

Hi There! 

I'm excited for the chance to join the Datadog Support team! In addition to knowing DD by reputation as one of the best tech companies to work for in NY, I had the opportunity to speak with Scott Enriquez last week -- he generously helped me understand more about the team and the work, and confirmed my suspicions that it is a great role at a great company.
 
While my background is in math and data analytics I currently work in a customer-facing role at a startup, providing a DevOps platform for data scientists. I believe that my track record working with a highly technical clientele to understand their infrastructure needs and communicate the capabiliteis of our solution will make me an asset to the Support Engineering team at Datadog.

More info can be found on [my Linkedin](https://www.linkedin.com/in/samxjacobs).

That's probably more than enough bio -- let's get started!

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

The Agent check that we wrote in the last section should be sampling and sending results every 15 seconds.

We can visualize this by creating a graph of this metric in a dashboard. To do so, we can clone the dashboard of our Postgres db from the host map and find the resulting dashboard at [https://app.datadoghq.com/dash/list](https://app.datadoghq.com/dash/list)

Once on the "Postgres Overview -- Cloned" dashboard, we can add a graph using the "Add Graph" button at the top of the page, and create a timeseries graph reporting the test.support.random metric.

![Metric Graph](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/metric_reporting.png?raw=true)

## Bonus: What is the difference between a timeboard and a screenboard?

Datadog dashboards can be defined as either a timeboard or a screenboard. The defining feature of a timeboard is that all graphs are scoped to the same time. This facilitates troubleshooting and correlation across metrics. 

The screenboard relaxes this condition, and also alllows for a more flexible layout of graphs. This makes it easy to take in the metrics that you have deemed important at a glance.

## Snapshots and Event Notifications

Once we have created a graph, we can annotate points of interest using the camera icon at the top right of the graph to selct regions of the display. These annotations can be shared with others on the team using the pattern @{team_member_name} in our comment. These annotations are added to the event stream, and emails or other 3rd party notifications are sent to teammates tagged uisng the @notificaion:

![Event stream notification](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/snapshot_with_at_notification.png?raw=true)

# Alerting on our data

## Setting up the monitor

Often a metric is of interest only if it is not behaving in ordinary boundaries. Conveniently, we can create monitors that alert members of the team if certain conditions are met by a gieven metric. New monitors can be created at [https://app.datadoghq.com/monitors#create/metric](https://app.datadoghq.com/monitors#create/metric) while existing metrics can be managed at [https://app.datadoghq.com/monitors#manage](https://app.datadoghq.com/monitors#manage). A detailed guide to setting up monitors can be found [here](http://docs.datadoghq.com/guides/monitoring/).

Monitors can be defined on particular metrics and metric aggregations across subsets of the the infrastructure, time, and the team. 

As an example, let's create a monitor that

1. alerts team member @smjacob4@asu.edu 
2. if the max value of test.support.random exceeds 0.9
3. on any host in the infrastructure
4. per 5minute window
5. between 9am and 7pm EST

## Bonus: Multi-alerts!

While an alert can be set on a particular host, it is possible to create a generic alert to be set on all hosts with a given tag, called a multi-alert. This is done  in the "New Monitor +" menu, as shown below. In this case, we will configure this monitor to be set on each host in our infrastructure:

![Set it as a multi alert](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/multi_alert_setting.png?raw=true)

## Monitor Message and Email notification

Monitors can be set to notify specific members of the team when an alert is triggered, using the same @notification format we used to share a snapshot. Once our monitor is reporting, we can see what this alert email will look like:

![Alert email notification](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/alert_triggered.png?raw=true)

## Bonus: Scheduling Downtime

Just as a monitor can be set to only trigger on hosts with certain tags, it can also be set to only trigger during specific timewindows. This can be done on the "Manage Down time tab" found at [https://app.datadoghq.com/monitors#/downtime](https://app.datadoghq.com/monitors#/downtime). 

Downtime can be scheduled either one-off or on a repeating interval. In this case, let's set our trigger to be silent between 7pm and 9am, so we can get some sleep :)

![Make it repeat](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/downtime_repeating.png?raw=true))

Using @notifications, other members of the team can be updated when the downtime conditions on an alert are changed, as shown below.

![Send an email notification](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/downtime_notification.png?raw=true)



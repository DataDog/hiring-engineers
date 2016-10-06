Your answers to the questions go here.

# Level 0 - Setting up Ubuntu

To ensure that we won't run into any OS or dependency issues, we'll start by create a new virtual machine running Ubuntu. After installing Virtual Box and Vagrant, this can be done with the command

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

Tags are user-created, nominal dimensions that make it easier to group and filter hosts within an infrastructure. There are a few sorts of tags, but fo rnow let's restrict ourselves to Agent tags. We'll tag our agent by adding this line to the agent config file, found (on linux) at /etc/dd-agent/datadog.conf:

```
tags: firstname:sam, lastname:jacobs, hello:world
```

Tags are often structured as key/value pairs, but this is not a requirement. After we've altered the config, we must update the agent by running

```
vagrant$ sudo /etc/init.d/datadog-agent restart
```

We can see these chages reflected in the Datadog UI on the Host Map (https://app.datadoghq.com/infrastructure/map)

![Agent reporting for duty](https://github.com/PerplexedSphex/hiring-engineers/blob/support-engineer/screenshots/Tags.png?raw=true)

## Database Integrations



  

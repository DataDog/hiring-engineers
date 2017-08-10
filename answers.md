

## Table of Contents

- [Launching an Ubuntu VM](#launching-an-ubuntu-vm)
- [Collecting Your Data](#collecting-your-data)
  - [Installing Datadog-Agent on Ubuntu](#installing-datadog-agent-on-ubuntu)
    - [Installing an Agent Directly](#installing-an-agent-directly)
    - [Installing and Launching a Docker Container](#installing-and-launching-a-docker-continer)
  - [Tagging Your VM](#tagging-your-vm)
  - [Installing & Monitoring PostgreSQL](#installing--monitoring-postgresql)
  - [Installing & Monitoring Docker](#installing--monitoring-docker)
  - [Writing a Custom Agent Check](#writing-a-custom-agent-check)
- [Visualizing Data](#visualizing-data)
  - [PostgreSQL Dashboard](#mongo-dashboard)
  - [Snapshot and Annotation](#snapshot-and-annotation)
- [Alerting on Data](#alerting-on-data)
  - [Create a Monitor](#create-a-monitor)
  - [Email Screenshot](#email-screenshot)
  - [Night Time Down Time](#night-time-down-time)
- [Conclusion](#conclusion)
- [Bonus Questions](#bonus-questions)
- [Found Syntax Errors](#found-syntax-errors)


# Launching an Ubuntu VM

[KVM](https://wiki.qemu.org/Features/KVM) also known as Kernel Virtual Machine is a Linux kernel module that allows a user space program to utilize the hardware virtualization features of various processors.

To install KVM on Ubuntu follow the link below:

[Install KVM](https://www.cyberciti.biz/faq/installing-kvm-on-ubuntu-16-04-lts-server/)

Once KVM is installed here is a small script that will install the latest version of the Ubuntu LTS iso. Then begin creating the Ubuntu vm with memory=1GB, cpu=1, and storage=15GB. To complete the install a vnc window will appear. Follow the Ubuntu guided install to finish building your vm.

`cd /var/lib/libvirt/boot/ && \
sudo wget https://www.ubuntu.com/download/server/thank-you?version=16.04.3&architecture=amd64 && \
sudo virt-install \
--virt-type=kvm \
--name=ubuntu_xenial \
--ram=1024 \
--vcpus=1 \
--os-variant=ubuntu \
--virt-type=kvm \
--hvm \
--cdrom=/var/lib/libvirt/boot/ubuntu-16.04.3-server-amd64.iso \
--network=bridge=br0,model=virtio \
--network=bridge=br1,model=virtio \
--graphics vnc \
--disk path=/var/lib/libvirt/images/ubuntu_xenial.qcow2,size=15,bus=virtio,format=qcow2`

# Collecting Your Data

## Installing Datadog-Agent on Ubuntu

### Installing an Agent Directly
Datadog can be installed on most operating systems distributions available today. You can find the list of supported operating systems and their installation guides [here](https://app.datadoghq.com/account/settings#agent).

There is a quick setup one-line install for each operating system platform. As an example the Ubuntu one-line will resemble the code below. Of course remember to change the API Key to your own.

`DD_API_KEY={Insert Your API Key} bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"`

### Installing and Launching Agent in Docker Container

The Datadog-agent can also be added to existing docker deployments. Reasons for using a docker container apposed to directly installing the agent are speed, compatibility and easy of deploy.

At times it is much faster to pull a docker image that is set up to meet the monitoring requirements to a specific host or set of hosts you wish to monitor. Introducing a Datadog-agent container to a swarm configuration will make deploying and monitoring your docker stack a simple push button solution.

* You can get a copy of the Datadog docker image with the following command.
`docker pull datadog/docker-dd-agent`

* Then once you have the imaged pulled go ahead and run it. Remember to change the API_KEY to your key.

`docker run -d --name dd-agent \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -v /opt/dd-agent-conf.d:/conf.d:ro \
  -e API_KEY={Insert Your API Key} \
  -e SD_BACKEND=docker \
  -e TAGS=docker-dd-agent,domain:stuffnthings.io,role:registry \
  datadog/docker-dd-agent`

### Quick Docker Explanation
* First the line `docker run -d --name dd-agent` will detach the container and then print the container's id and name the running container **dd-agent**.

* The next four lines are volume mappings. They map paths on the host to paths in the container.
  - `-v /var/run/docker.sock:/var/run/docker.sock:ro` This is the unix socket used to communicate with the daemon located within the container.

  - `-v /proc/:/host/proc/:ro \` This mapping is key to giving the agent all the data from the host it is supposed to auto discover. One key piece of information is the hostname that is found at **/proc/sys/kernel/hostname:gateway**.

  - `-v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \` This will map the container to use the cgroup of the host. You can find information about memory and cpu usage here. This will be mapped as read only.

  - `-v /opt/dd-agent-conf.d:/conf.d:ro \` Here is the integration conf.d for the datadog-agent.

* The final three lines are environment variables that fill in entries of the datadog.conf file. API key, tags, and autodiscovery configuration insertions.

## Tagging Your VM
## Installing & Monitoring PostgreSQL
## Installing & Monitoring Docker
## Writing a Custom Agent Check




# Conclusion
This project was one of the most fun technical assessments I have ever worked on. It opened my eyes to how robust and easy to use Datadog software can be. I'm really eager to receive more complicated problems that can really push my limits to the next level.


# Bonus Questions
> Bonus question #1: In your own words, what is the Agent?

An agent is a service that is constantly collecting data. The data the agent is collecting can vary, but is mostly metric data such as physical disk information (i.e mount name, type, size, used, free, total), system information (i.e hostname, OS version, up time), Memory Status (i.e used, free, total), etc. Periodically the Datadog agent will send this data to your private Datadog centralized service.

In my own words the Datadog agent is a "secret agent" out in the field collecting information Datadog "HQ" can keep tabs on difference hosts "targets". So if the target goes rogue (triggers a threshold) the agent will alert HQ so that it can alert the special forces to secure the target.


# Found syntax errors

##### Currently
`psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"
 && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ ||
echo -e "\e[0;31mCannot connect to Postgres\e[0m"`

There are two mistakes in this script that tests the connection of the read only user "datadog" in a PostgreSQL integration.
1. There is no trailing `\` at the end of the first line. This will cause the first line to complete without executing the '&&' that ties the lines together. Normally this wouldn't be a problem if the script was on a single line, but to make this truely copy & paste friendly the trailing `\` is really necessary.
2. The next error here is on the second line. The `|| \ ||` will fail. You can't test to see if an OR will fail to another OR. The solution is to remove the `||` at the end.

##### Should be
`psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" \
 && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
echo -e "\e[0;31mCannot connect to Postgres\e[0m"`

This is as it should be, truly copy & paste friendly.

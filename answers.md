# Datadog Technical Exercise - Jeremy LaBrosse

In this exercise we're being asked to demonstrate the Datadog monitoring suite.  It calls for the creation of a single VM, however, in Devops we strongly prefer to deploy things automatically such that we can support any number of VMs.  There are many ways this automation can be achieved.  For the purposes of this demonstration we're going to show an example of how it can be done in Ansible using VMs created in Amazon's AWS cloud.

## Table of Contents

- [Installation](#installation)
  - [VM Creation](#vm-creation)
  - [Ansible Setup](#ansible-setup)
  - [Datadog Agent Install](#datadog-agent-install)
  - [Dynamic Inventory](#dynamic-inventory)
- [Data Collection](#data-collection)
  - [Datadog vs Nagios](#datadog-vs-nagios)
  - [Bonus Question: What is the Agent?](#bonus-question-what-is-the-agent)
  - [Tagging](#tagging)
  - [Install MySQL](#install-mysql)
    - [Ansible Install of MySQL](#ansible-install-of-mysql)
  - [Create a Custom Check](#create-a-custom-check)
    - [Ansible Install of Random Check](#ansible-install-of-random-check)
- [Data Visualization](#data-visualization)
  - [Create a Dashboard](#create-a-dashboard)
  - [Bonus Question: Timeboard vs Screenboard?](#bonus-question-timeboard-vs-screenboard)
  - [Custom Check Snapshot](#custom-check-snapshot)
- [Monitoring and Alerting](#monitoring-and-alerting)
  - [Create a Monitor and Alert](#create-a-monitor-and-alert)
  - [Bonus: Schedule Downtime](#bonus-schedule-downtime)
- [Conclusion](#conclusion)
- [Personal Notes](#personal-notes)

## Installation

### VM Creation

We will use the Amazon AWS free tier to create three t2.micro VMs: a RHEL 7.4 Ansible server, an Ubuntu 14.04 host called randomserver01, and a RHEL 7.4 host called randomserver02.  This way we can demonstrate that this automation setup is agnostic with regards to the operating system.  We will use the Ansible server to install the Datadog agent on all three VMs, including itself.  We will also use it to deploy MySQL and the MySQL integration, as well as the custom random check script and integration, to the two randomserver hosts.

![AWS Host List](https://user-images.githubusercontent.com/31740703/30281770-4b57f632-96e1-11e7-830e-00ea9d082009.png)

### Ansible Setup

First we need to install Ansible on the Ansible server.  For RHEL 7.4 the Ansible package comes from the EPEL repo, so we'll also have to install that.

```
# sudo yum install –y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

(output truncated)

Installed:
  epel-release.noarch 0:7-10

# sudo yum install -y ansible

(output truncated)

Installed:
  ansible.noarch 0:2.3.1.0-1.el7
```

We can use ansible-galaxy to install the Datadog agent role.

```
# ansible-galaxy install Datadog.datadog
- downloading role 'datadog', owned by Datadog
- downloading role from https://github.com/DataDog/ansible-datadog/archive/1.3.0.tar.gz
- extracting Datadog.datadog to /etc/ansible/roles/Datadog.datadog
- Datadog.datadog (1.3.0) was installed successfully
```

Normally we would have the hosts registered with Route 53 DNS so Ansible could resolve the hostnames.  For this demonstration it will be easier to hard code the IP addresses in the /etc/hosts file on the Ansible server.

```
$ cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
# Ansible server local IP - RHEL 7.4
172.31.9.117	ansible
## randomserver01 - Ubuntu 14.04
172.31.4.43	randomserver01
## randomserver02 - RHEL 7.4
172.31.14.170	randomserver02
```

We will also populate the Ansible hosts inventory file manually.  We will set two hostgroups: ansibleservers, and randomservers.

```
$ cat /etc/ansible/hosts
[ansibleservers]
# RHEL 7.4
ansible

[randomservers]
# Ubuntu 14.04
randomserver01
# RHEL 7.4
randomserver02
```

This is the complete Ansible tree with all the roles, plays, vars, and templates.  We will describe each of the individual files as we need to use them.

```
# tree /etc/ansible
/etc/ansible
├── ansible.cfg
├── group_vars
│   └── all
│       ├── vars
│       └── vault
├── hosts
├── plays
│   ├── datadog.yml
│   ├── mysql.yml
│   └── random.yml
└── roles
    ├── Datadog.datadog
    │   ├── CHANGELOG.md
    │   ├── defaults
    │   │   └── main.yml
    │   ├── handlers
    │   │   └── main.yml
    │   ├── meta
    │   │   └── main.yml
    │   ├── README.md
    │   ├── tasks
    │   │   ├── main.yml
    │   │   ├── pkg-debian.yml
    │   │   └── pkg-redhat.yml
    │   ├── templates
    │   │   ├── checks.yaml.j2
    │   │   ├── datadog.conf.j2
    │   │   ├── datadog.repo.j2
    │   │   └── process.yaml.j2
    │   └── tests
    │       └── test.yml
    ├── mysql
    │   ├── handlers
    │   │   └── main.yml
    │   ├── tasks
    │   │   ├── main.yml
    │   │   ├── pkg-debian.yml
    │   │   └── pkg-redhat.yml
    │   └── templates
    │       ├── mysql_setup.sh.j2
    │       └── mysql.yaml.j2
    └── random
        ├── handlers
        │   └── main.yml
        ├── tasks
        │   └── main.yml
        └── templates
            ├── random.py.j2
            └── random.yaml.j2
```

It should be noted that Ansible also requires the pushing of SSH keys to the client servers, which for this demonstration will be done manually.

### Datadog Agent Install

In order to install the agent we need two things: the Datadog.datadog role, which we installed via ansible-galaxy, and a playbook to call it.  This is the playbook.

```
# cat /etc/ansible/plays/datadog.yml
---

- hosts: all
  roles:
    - { role: Datadog.datadog, become: yes }
```

Then we call it from the command line using the ansible-playbook command.  The outputs from Ansible runs can be very long and verbose and typically don't contain anything necessary to see unless there is an error.  For this demonstration we will truncate the output.

```
# ansible-playbook plays/datadog.yml -i hosts

PLAY [all] *********************************************************************************

TASK [Gathering Facts] *********************************************************************
ok: [ansible]
ok: [randomserver01]
ok: [randomserver02]

(output truncated)

PLAY RECAP *********************************************************************************
ansible                    : ok=8    changed=7    unreachable=0    failed=0
randomserver01             : ok=9    changed=7    unreachable=0    failed=0
randomserver02             : ok=8    changed=7    unreachable=0    failed=0
```

After this we just have to wait a few minutes and the hosts will show up in the Datadog UI automatically with their hostnames and tags already set.

![Datadog Host Map](https://user-images.githubusercontent.com/31740703/30282062-2bd132a0-96e2-11e7-93d2-4b607cff40d5.png)

### Dynamic Inventory

Incidentally, it would not be very difficult to make the Ansible hosts inventory dynamic.  With a dynamic inventory we could take advantage of automated services to instantiate new servers, such as the AWS autoscalers, which Ansible could then automatically update and pull into our Datadog setup.  As a simple example, Ansible can make an AWS CLI call to get the current list of VM instance IDs and associated AWS tags.

```
$ aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,Tags[*]]' --output text

i-0e3ae8cdd26ecfbf4
Type	ansible
Name	ansible

i-0eb9bec546ce92e92
DB	mysql
Type	random
Name	randomserver01

i-0848eb9f026a1c934
DB	mysql
Type	random
Name	randomserver02
```

There are many possible approaches.  We would likely want to integrate this with other automation tools, such as Packer for building AMIs and Terraform for instantiating the networks, DNS, VMs, autoscaling groups, etc.  We're going to skip that for now since it's too far out of scope for this demonstration.

## Data Collection

### Datadog vs Nagios

One of the key differences between Datadog and Nagios is that Datadog splits data collection and monitoring/alerting into two separate phases.  In Nagios these two concepts are basically commingled.  Each Nagios check can be thought of as looking to see if we should alert each time it fires.  In practice, in the past, when we've wanted to visualize the long term trend of a Nagios check that we don't necessarily want to be alerted on we have had to pair Nagios with a graphical add-on, such as PNP or Graphite, and then permanently disable notifications for that check.  The Datadog agent provides data to Datadog which can be visualized graphically directly via the UI.  Setting up a monitor and alert is done in a completely separate phase.

### Bonus Question: What is the Agent?

The agent is a daemon that runs in the background collecting system and application data and continuously sends it to Datadog.  It pulls system data from StatsD, which already provides more information than Nagios typically collects, and also pulls application data from an embedded daemon called DogStatsD to make setting up custom checks simple.

### Tagging

We set the hostname for the Datadog UI and the host tags with Ansible by injecting variables into the Datadog.datadog role.  Those values are stored in the group_vars/all/vars with the passwords being kept in an encrypted vault file.  Ansible uses Jinja for variables which uses a double curly brace format.  We will be setting up three specific tags for filtering in the Datadog UI: hostname, function (ansible hostgroup), and os type.

```
# cat /etc/ansible/group_vars/all/vars
# Datadog variables
datadog_api_key: "{{ vault_datadog_api_key }}"
datadog_mysql_password: "{{ vault_datadog_mysql_password }}"
datadog_config:
  hostname: "{{ inventory_hostname }}"
  tags: "hostname:{{ inventory_hostname }}, function:{{ group_names[0] }}, os:{{ ansible_os_family }}"
  log_level: INFO
```

We can sort our hosts by the tags we've created.

![Tag sorting](https://user-images.githubusercontent.com/31740703/30281790-5ab12e64-96e1-11e7-8e44-4c2aa947842e.png)

### Install MySQL

We will install MySQL and its Datadog integration via the same Ansible role.  The role requires a few elements.  We'll need two package install plays, one for debian and one for redhat.  We'll need a main play that calls them and also pushes and runs the MySQL configuration script.  We'll need a handler to start/restart MySQL.  And of course we'll have to push the Datadog configuration yaml file that enables the third party integration.

Package installers:

```
# cat /etc/ansible/roles/mysql/tasks/pkg-debian.yml
---

- name: Install mysql-server
  apt: name=mysql-server state=present
  register: mysqld_installed
  when: ansible_os_family == "Debian"

---
- name: Run mysql_install_db
  shell: mysql_install_db
  when: mysqld_installed.changed


# cat /etc/ansible/roles/mysql/tasks/pkg-redhat.yml
---

- name: Install mysql repo via remote RPM
  yum:
    name: http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
    state: present

- name: Install mysql-server
  yum: name=mysql-server state=present
  register: mysqld_installed

- name: Enable mysqld after install
  shell: systemctl enable mysqld
  when: mysqld_installed.changed
  notify: restart mysqld
```

The main play:

```
# cat /etc/ansible/roles/mysql/tasks/main.yml
---

- include: pkg-debian.yml
  when: ansible_os_family == "Debian"

- include: pkg-redhat.yml
  when: ansible_os_family == "RedHat"

- name: Push mysql_setup.sh script
  template: src=mysql_setup.sh.j2 dest=/root/mysql_setup.sh owner=root group=root mode=0744

- name: Run mysql_setup.sh on install
  shell: /root/mysql_setup.sh
  when: mysqld_installed.changed

- name: Push mysql.yaml configs
  template: src=mysql.yaml.j2 dest=/etc/dd-agent/conf.d/mysql.yaml owner=dd-agent group=dd-agent mode=0644
  notify: restart datadog-agent
```

Restart handler:

```
# cat /etc/ansible/roles/mysql/handlers/main.yml
---

- name: restart mysqld
  action: service name=mysqld state=restarted

- name: restart datadog-agent
  action: service name=datadog-agent state=restarted
```

The MySQL setup script that gives the appropriate permissions for the Datadog agent:

```
# cat /etc/ansible/roles/mysql/templates/mysql_setup.sh.j2
mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY '{{ datadog_mysql_password }}';"
mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
mysql -u datadog --password={{ datadog_mysql_password }} -e "show status" | \
grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
echo -e "\033[0;31mCannot connect to MySQL\033[0m"
mysql -u datadog --password={{ datadog_mysql_password }} -e "show slave status" && \
echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
mysql -u datadog --password={{ datadog_mysql_password }} -e "SELECT * FROM performance_schema.threads" && \
echo -e "\033[0;32mMySQL SELECT grant - OK\033[0m" || \
echo -e "\033[0;31mMissing SELECT grant\033[0m"
mysql -u datadog --password={{ datadog_mysql_password }} -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST" && \
echo -e "\033[0;32mMySQL PROCESS grant - OK\033[0m" || \
echo -e "\033[0;31mMissing PROCESS grant\033[0m"
```

This is the configuration file that enables the third party integration in Datadog.  It goes in the /etc/dd-agent/conf.d directory.

```
# cat /etc/ansible/roles/mysql/templates/mysql.yaml.j2
init_config:

instances:
  - server: localhost
    user: datadog
    pass: {{ datadog_mysql_password }}

    tags:
      - mysql_server
    options:
      replication: 0
      galera_cluster: 1
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
```
#### Ansible Install of MySQL

We install this role by calling the playbook with ansible-playbook, similar to installing the agent.

```
# cat /etc/ansible/plays/mysql.yml
---

- hosts: randomservers
  roles:
    - { role: mysql, become: yes }
```

```
# ansible-playbook plays/mysql.yml -i hosts

PLAY [randomservers] *************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************
ok: [randomserver01]
ok: [randomserver02]

(output truncated)

PLAY RECAP ***********************************************************************************************************************************************************
randomserver01             : ok=4    changed=0    unreachable=0    failed=0
randomserver02             : ok=5    changed=0    unreachable=0    failed=0
```

### Create a Custom Check

Installing a custom check via Ansible will follow a similar procedure, however, since there is no package to install it should be much simpler.  We will need a main play to push two configuration files: a python check file to /etc/dd-agent/check.d, and the /etc/dd-agent/conf.d configuration yaml file which enables the third party integration.

```
# cat /etc/ansible/roles/random/tasks/main.yml
---

- name: Push random.py script
  template: src=random.py.j2 dest=/etc/dd-agent/checks.d/random.py owner=dd-agent group=dd-agent mode=0644

- name: Push random.yaml configs
  template: src=random.yaml.j2 dest=/etc/dd-agent/conf.d/random.yaml owner=dd-agent group=dd-agent mode=0644
  notify: restart datadog-agent
```

The check file contains the actual code that will be executed.  Please note that the check and configuration files will have the same basenames.

```
# cat /etc/ansible/roles/random/templates/random.py.j2
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

The configuration yaml file is similar to the one we pushed for MySQL.

```
# cat /etc/ansible/roles/random/templates/random.yaml.j2
init_config:
  min_collection_interval: 30
instances:
  [{}]
```

#### Ansible Install of Random Check

We install this role by calling the playbook with ansible-playbook, like we did with the agent and MySQL roles.

```
# cat /etc/ansible/plays/random.yml
---

- hosts: randomservers
  roles:
    - { role: random, become: yes }
```

```
# ansible-playbook plays/random.yml -i hosts

PLAY [randomservers] *************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************
ok: [randomserver01]
ok: [randomserver02]

TASK [random : Push random.py script] ********************************************************************************************************************************
changed: [randomserver01]
changed: [randomserver02]

TASK [random : Push random.yaml configs] *****************************************************************************************************************************
changed: [randomserver01]
changed: [randomserver02]

RUNNING HANDLER [random : restart datadog-agent] *********************************************************************************************************************
changed: [randomserver01]
changed: [randomserver02]

PLAY RECAP ***********************************************************************************************************************************************************
randomserver01             : ok=4    changed=3    unreachable=0    failed=0
randomserver02             : ok=4    changed=3    unreachable=0    failed=0
```

## Data Visualization

### Create a Dashboard

We can clone the database integration dashboard via the Datadog UI so we can customize it and add additional database metrics and the random check metrics to suit our needs.

![Custom Dashboard](https://user-images.githubusercontent.com/31740703/30281798-60b3592c-96e1-11e7-8e2c-bcccafa0492d.png)

### Bonus Question: Timeboard vs Screenboard?

The Timeboard displays metrics and graphs in an automated grid layout, all of which are automatically synced to the same time.  This gives us the ability to troubleshoot by seeing the correlation of concurrent events.  The Timeboard is more limited than the Screenboard in terms of what it can show and the graphs can only be shared individually.

The Screenboard brings together a larger set of options for graphs and drag-and-drop widgets that are not necessarily time-synced.  The layout is flexible and the entire Screenboard can be shared out, even read-only.  This helps provide a more comprehensive view of the system.

### Custom Check Snapshot

We can take a snapshot of any metric, leave a comment, and ensure that it gets broadcast to the right people.

![Custom Check Snapshot](https://user-images.githubusercontent.com/31740703/30281815-6fb6bca2-96e1-11e7-9ebe-faf6cdbe8e94.png)

## Monitoring and Alerting

### Create a Monitor and Alert

We want to set up a monitor for our random check because we don't want to watch the dashboard live.  We'll also want to set up an alert to send us an email if it goes above 0.9 again so we can be made aware.  By making it a multi-alert that triggers for each host the monitor will automatically scale for all servers using the test.support.random metric.

![Custom Monitor and Alert 1](https://user-images.githubusercontent.com/31740703/30281822-76ee0c50-96e1-11e7-90cb-11a814419d25.png)
![Custom Monitor and Alert 2](https://user-images.githubusercontent.com/31740703/30281826-7911c51c-96e1-11e7-9c2a-9fa99bb0193b.png)

### Bonus: Schedule Downtime

We've been told that we don't want to be alerted for this monitor after hours, so we can arrange downtime.

![Scheduled Downtime](https://user-images.githubusercontent.com/31740703/30281831-7fb9bc94-96e1-11e7-945e-868e5f3ae276.png)
![Scheduled Downtime Email](https://user-images.githubusercontent.com/31740703/30281843-8690e2d6-96e1-11e7-9813-d30b608efe1e.png)

## Conclusion

Using Ansible to deploy Datadog takes a bit of initial setup time, especially since Ansible can be finicky about its configs, but once it's set up it empowers us to rapidly deploy monitoring to new hosts in an automated fashion.  The setup we built here can theoretically deploy an unlimited amount of hosts, although the Datadog free trial only allows up to 5 hosts to be monitored.

## Personal Notes

This was a fun project.  I had already done some of this in my current job.  I did the initial internal demo to help sell Datadog to our management team and then later I was materially involved in the automated roll out of the agent to our fleets via Ansible.  As a Senior Devops Engineer I feel that part of my duties include writing and giving training on new technologies that we roll out, especially when it relates to logging and monitoring.  We fully implemented Datadog exclusively in the cloud and dropped all of our Nagios resources, so I have been planning on giving training on it to the engineering teams after the cutover.  Ultimately, these tools aren't for me, they are for the engineers.  One of the goals of Devops is to close the feedback loop for the developers so they can do their own operational work without relying on an external Ops team.  They can also get a better sense of the actual performance of the website and their code changes.

This technical exercise gave me a fantastic view into several areas I hadn't previously gotten a lot of direct exposure to, specifically around third party integrations, custom checks, and dashboarding.  My goal is to help the developers feel comfortable and confident writing their own checks and dashboards and responding to alerts for the products they build.  The goal is to shift the responsibility and pride of ownership back onto the subject matter experts who write the code.  This exercise has helped me make that a practical reality.



# Datadog technical exercise for Solutions Engineers

Datadog is a full service cloud-scale monitoring solution that gathers metrics and events generated by both your infrastructure
as well as your applications. From containers, to cloud providers, to bare metal machines, from container management, to databases, to web servers,
datadog is able to handle most modern infrastructure solutions.

Datadog provides a wide array of integrations that can handle common infrastructure needs. These integrations allow you to gather metrics 
quickly and in one central location. All metrics and statistics datadog gathers can be displayed in a single pane of glass which can be on a single
screen in a NOC or other operations center. These metrics can be turned into graphs and dashboards which can then be drilled down into further for 
a more detailed look at your infrastructure. Alerts can also be created to warn your teams that something is wrong before it becomes a larger problem.
Alerts can be sent in a variety of ways, including email, pagerduty, slack, hipchat, and others.

You can test datadog out yourself here [https://www.datadoghq.com/](https://www.datadoghq.com/) for a free 14 day trial.

## Contents

- [Prerequisites](#Prerequisites)
   - [Setup an AWS user for Terraform](#Setup-an-AWS-user-for-Terraform)
   - [Install Terraform](#Install-Terraform)
   - [Install Ansible](#Install-Ansible)

- [Data Collection](#Data-Collection)
   - [Level 0 - Setup a ubuntu instance](#Level--0--Setup-a-ubuntu-instance)
      - [Auto build EC2 instance with Terraform](#Auto-build-EC2-instance-with-Terraform)

   - [Level 1 - Collect your data](#Level--1--Collect-your-data)
      - [Auto installing the agent with Ansible](#Auto-installing-the-agent-with-Ansible)
      - [Bonus: What is the agent?](#Bonus--What-is-the-agent?)
      - [Adding tags](#Adding-tags)
      - [Auto install MySQL with Ansible](#Auto-install-MySQL-with-Ansible)
      - [Custom Agent Check](#Custom-Agent-Check)

   - [Level 2 - Visualizing your data](#Level--2--Visualizing-your-data)
      - [Clone your database integration dashboard](#Clone-your-database-integration-dashboard)
      - [Bonus: What is the difference between a timeboard and a screenboard?](#Bonus--What-is-the-difference-between-a-timeboard-and-a-screenboard?)
      - [Grab a snapshot of your test random graph, draw a box when above 0.90 and email](#Grab-a-snapshot-of-your-test-random-graph,-draw-a-box-when-above-0.90-and-email)

   - [Level 3 - Alerting on your data](#Level--3--Alerting-on-your-data)
      - [Monitoring your metrics, set an alert for test random for over 0.90](#Monitoring-your-metrics,-set-an-alert-for-test-random-for-over-0.90)
      - [Bonus: Make it multi-alert by host for scalability](#Bonus--Make-it-multi-alert-by-host-for-scalability)
      - [Set monitor name and message](#Set-monitor-name-and-message)
      - [Monitor alert Email](#Monitor-alert-Email)
      - [Bonus: Set scheduled downtime for monitor, make sure Email is notified](#Bonus--Set-scheduled-downtime-for-monitor,-make-sure-Email-is-notified)

- [Conclusion](#Conclusion)

# Prerequisites

## Setup an AWS user for Terraform

- Setting up an AWS user for Terraform [Amazon Web Services(AWS)](https://aws.amazon.com/) is the leading cloud compute provider. 
  They offer a wide range of infrastructure services.
- Create a user in IAM, there are three steps to follow to create an IAM user to use with Terraform. 
- One, give the user a name and make sure they have programmatic access only. There's no need for console access with Terraform.

![Create_AWS_User_Step1](screenshots/Create_AWS_User_Step1.png)

- Two, in order to have Terraform create our EC2 instance we'll need the proper AWS permissions. For this user they will need only 
  **AmazonEC2FullAccess** in order to create and destroy EC2 instances.

![Create_AWS_User_Step2_Permissions](screenshots/Create_AWS_User_Step2_Permissions.png)

- Finally, You will need both the access and secret keys for the user. These will be used at runtime so as to not save them in a file and cause a security risk.

![Create_AWS_User_Step3_Keys](screenshots/Create_AWS_User_Step3_Keys.png)

## Install Terraform

- [Installing Terraform](https://www.terraform.io/downloads.html) Terraform is much more then just a configuration management tool. It lets you define your 
  infrastructure as code. Download it for your appropriate OS.

- Download the correct version of Terraform for your OS, I have downloaded **terraform_0.10.3_darwin_amd64.zip** for MacOSX. Unzipping inflates the file you then move that file 
  to somewhere that is in your PATH. I have moved the file to **/usr/local/bin** which lets me access the terraform command directly.

## Install Ansible

- [Installing Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html) Ansible is an open source configuration management tool. Powerful but yet extremely simple to use.
  Ansible can handle not only configuration management but application deployments, and task automation. Installation instructions are dependent on OS used.

- Since I am installing on MacOSX I will be using pip which is python's package manager. You can install pip by downloading this file [Pip](https://bootstrap.pypa.io/get-pip.py) 
  and running python get-pip.py. 

- Now that you have pip you can install ansible by simply running **sudo pip install ansible** this will install ansible and a series of other applications. We'll mainly concentrate on 
  ansible-playbook.

# Data Collection

## Level 0 Setup an Ubuntu Instance

## Auto build EC2 instance with Terraform

- We will auto build our EC2 instance that will run our database, as well as our datadog agent. This will be a t2.large EC2 instance in AWS. We will build this with Terraform

- The code below will build our instance for us.

```terraform
provider "aws" {
  access_key    = "${var.access_key}"
  secret_key    = "${var.secret_key}"
}   
   
resource "aws_instance" "Datadog_Tech_Example" {
  ami                         = "ami-cd0f5cb6"
  instance_type               = "t2.large"
  associate_public_ip_address = true
  key_name                    = "DD_Testing"
  vpc_security_group_ids = [
      "sg-033ebf73"
  ]

  tags {
    Name = "Datadog_Tech_Example"
  }

  provisioner "local-exec" {
    command = "sleep 120; ANSIBLE_HOST_KEY_CHECKING=False AWS_ACCESS_KEY=${var.access_key} AWS_SECRET_KEY=${var.secret_key} ansible-playbook /Users/hack/dd_solution_engineer/ansible/Tasks/main.yml -u 	ubuntu --private-key /Users/hack/.ssh/DD_Testing.pem -i '${aws_instance.Datadog_Tech_Example.public_ip},'"
  }
}
```

- A short overview of the code above, we set the provider to be AWS (terraform can also be used with other cloud providers such as google). For the access and secret keys we will use the ones we
  generated earlier for the user. These will be input during run-time. We are going to build an aws_instance resource called **Datadog_Tech_Example**, we are using the Ubuntu 16.04 AMI,
  its size will be t2.large, we will give it a public IP address, and access it using a previously created ssh key. The newly created instance will be associated with a previously created
  security group that grants SSH access as well as access for the datadog agent to communicate on port 8125. Finally we tag it with a Name so we can see it in the AWS Console. We will go over the
  provisioner portion in the next step when we install both a MySQL database as well as the datadog agent itself.

## Level 1 Collect your data

## Auto installing the agent with Ansible

- We will use Ansible to install the agent on our host automatically. This will tie in with Terraform, we will create an ansible playbook that will be run by Terraform when our EC2 instance
  is created

```yaml
---
- hosts: all
  become: true
  gather_facts: False
  tasks:

    - name: Run dd-agent install script
      raw: DD_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

    - name: Copy the data dog conf file
      template:
        src: ../Templates/datadog.conf.j2
        dest: /etc/dd-agent/datadog.conf
        mode: 0640

    - name: Copy the data dog mysql conf.d yaml file
      template:
        src: ../Templates/mysql.yaml.j2
        dest: /etc/dd-agent/conf.d/mysql.yaml
        mode: 0644

    - name: Copy the sample random conf.d yaml file
      template:
        src: ../Templates/sample_random.yaml.j2
        dest: /etc/dd-agent/conf.d/sample_random.yaml
        mode: 0644

    - name: Copy the sample random python script
      template:
        src: ../Templates/sample_random.py.j2
        dest: /etc/dd-agent/checks.d/sample_random.py
        mode: 0644

    - name: Stop datadog agent
      command: /etc/init.d/datadog-agent stop

    - name: Start datadog agent
      command: /etc/init.d/datadog-agent start
```

- Reviewing this playbook, we use **hosts: all** as we wont know the EC2 hostname until creation, become sudo to run as root, we do not need to gather facts at this time.
  We then run the datadog installation one-liner (with API-KEY X'd out here). We have a copy of a datadog conf file setup already from an install by hand, we 
  copy this over with the correct permissions. We do the same thing with our database yaml file (in this case MySQL) our sample random yaml as well as our 
  actual sample random script. These are placed in their respective directories (conf.d for our yamls, checks.d for our agent check). We then restart our agent for these 
  additions to take effect.

## Bonus: What is the agent?

> The datadog agent is a collector, it collects data, events and metrics about your infrastructure and applications. It does this via pre-written checks and integrations that can be 
  used to monitor the majority of major platforms including cloud providers, databases, caching solutions, and web servers. The agent collects these metrics and events, and sends them 
  to datadog to be presented to you in a manner that will let you address pressing infrastructure issues whether they are immediate or something that will be taken care of in the future.
  Additionally custom checks can be written to monitor custom applications or to collect data that is in a non standard format.

## Adding tags

- Adding tags is a great way to identify and filter your infrastructure in datadog. Its as easy as updating the datadog.conf file, in the main section under host tags. Here is an example.

  ![Tag_Set_In_DDConf](screenshots/Tag_Set_In_DDConf.png)

  We can set individual tags as well as by environment or role or however you designate your infrastructure. Here we set a random tag **hacktag**, then an env tag and we put this host in
  the dev environment. We give this host the role of a web server, but we can make this what we want it
  to be if we have multiple database servers we can give it a role of database.

  Because we have installed this via Ansible and the agent has been restarted these tags are available from the start. You can see them if you click infrastructure -> infrastructure list 
  and then click your host. You can see an example below.

  ![Hostmap_tags_page](screenshots/Hostmap_tags_page.png)

  You can also see them via infrastructure -> Hostmap and clicking on your host. With the power of tags you are able to quickly search, distinguish, and filter your infrastructure per your needs. 

## Auto install MySQL with Ansible

- We will also be installing our database (MySQL) with Ansible. There are a couple of extra steps needed since this is the first file run when we build our instance. 
  Below is the file we will use to build out our database.

```yaml
---
- hosts: all
  become: true
  gather_facts: False
  tasks:
  - name: Load in vars
    include_vars:
      file: ../Defaults/main.yml

  - name: Install python 2 for ubuntu 1604
    raw: test -e /usr/bin/python || (apt -y update && apt install -y python-minimal)

  - name: apt-get update on first boot
    apt:
       update_cache: yes

  - name: Install MySql packages
    apt:
     name: "{{ item }}"
     state: installed
     update_cache: yes
    with_items: "{{ ubuntu_1604_mysql_pkgs }}"

  - name: Set MySql root password before installing
    debconf: name='mysql-server' question='mysql-server/root_password' value='{{ mysql_root_password | quote }}' vtype='password'

  - name: Confirm MySql root password before installing
    debconf: name='mysql-server' question='mysql-server/root_password_again' value='{{ mysql_root_password | quote }}' vtype='password'

  - name: Create datadog user in mysql db
    command: mysql -e "create user 'datadog'@'localhost' identified by '{{ mysql_datadog_user_password | quote }}';"

  - name: Grant replication rights to datadog user
    command: mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"

  - name: Grant full metrics to datadog user
    command: mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"

  - name: Grant access to performance schema to datadog user
    command: mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
```

- Since we run main task first when building the instance and since the first task run is to install MySQL we need to have two additions to this yaml file. First we load some vars which contain a list
  of the MySQL packages we will be installing. Secondly, we need to install python 2 for ubuntu 1604 as Ansible will throw an error if we only use python 3. We now update the cache on our ubuntu host, 
  then install the correct MySQL packages. As MySQL is being installed it will prompt the user for root password we have that automated as well by Ansible we set the password in the same file 
  that contains the vars and call that variable here identified by **mysql_root_password**. This needs to be confirmed and then we move on to creating the datadog user which will be used to report
  on the metrics of our database. The same var file contains the the datadog user password under the **mysql_datadog_user_password** variable. We grant the datadog user the proper permissions to 
  monitor our database and once the instance is up it with MySQL running it will be fully monitored.

## Custom Agent Check

- Creating a custom agent check is super easy with datadog, you can find more detailed instructions here [Datadog check creation](https://docs.datadoghq.com/guides/agent_checks/), but we can see a quick
  example below. 

- Our example will be a simple random sample check in python. The file that contains the logic of our check (in this example sample_random.py) will be placed in the **/etc/dd-agent/checks.d** directory. 
  While the configuration file for our check will live in **/etc/dd-agent/conf.d**. The configuration file will be in yaml while our checks can be written in python. There are API plugins for Ruby as well.

- Here is our sample_random.py file [sample_random.py.j2](ansible/Templates/sample_random.py.j2)
```python
from checks import AgentCheck
import random

class RandomCheck(AgentCheck):
	def check(self, instance):
		randNum = random.random()
		self.gauge('test.support.random', randNum)
```

- Since we have automated the install this check along with its configuration file is automatically installed in the correct directories once the agent is installed. You can see the results below.

![Custom_Check](screenshots/Custom_Check.png)

## Level 2 - Visualizing your data

## Clone your database integration dashboard

- Human beings are extremely good at recognizing patterns and irregularities within those patterns. This makes visualizing the data of an entire company's infrastructure so important, trying to
  read plain text log files to capture events simply will not scale as your company grows. 

- One of the benefits of datadog is the ability to create dashboards to gather these patterns in a visual manner for us. These can in turn be even more customized to fit different areas of your
  organization. There are two examples below, first is a very basic dashboard for our MySQL database and our sample_random script. These only contain four widgets, checking cpu time performance
  on our database instance as well as user performance time. The other two widgets are to check the change in our sample_random script and a graph of the sample_random output.

![Original_Dashboard](screenshots/Original_Dashboard.png)

- Second, if say a colleague uses your dashboard but needs additional information that pertains to their specific needs you can clone your dashboard and then edit this newly created dashboard.
  Below we have cloned our original dashboard above and added two new widgets, one to check on any "status:error" within our database, and the second to measure the number of connections there
  are to our database.

![Cloned_Dashboard](screenshots/Cloned_Dashboard.png)

- Cloning and adjusting your dashboards to fit the needs of the different teams monitoring your infrastructure can help make your responses to incidents more flexible and detailed.

## Bonus: What is the difference between a timeboard and a screenboard?

> A timeboard is used to correlate metrics and events to assist with troubleshooting. They are usually laid out in a specific way which in turn does not allow for much modification. 
  A screenboard is a more traditional screen you would see in a NOC or other operations center. They can be customized to a much greater degree then a timeboard. These are mainly used
  for displaying status data and providing a broad overview of your infrastructure.

## Grab a snapshot of your test random graph, draw a box when above 0.90 and email

![Graph_Over_Nine](screenshots/Graph_Over_Nine.png)

## Level 3 - Alerting on your data

## Monitoring your metrics, set an alert for test random for over 0.90

- Creating monitors to alert when something is wrong in your infrastructure is central to how datadog works. Below we setup a monitor to check when our Sample_Random script is above 0.90. 

![Monitor_Random_Over_Nine](screenshots/Monitor_Random_Over_Nine.png)

## Bonus: Make it multi-alert by host for scalability

- Scalability is an important part of monitoring, no one wants to reinvent the wheel every time a new host is brought up in your environment. We can set our Sample_Random check to multi-alert
  by host when we create our monitor. 

![Monitor_Random_Setup_Each_Host](screenshots/Monitor_Random_Setup_Each_Host.png)

## Set monitor name and message

- Setting unique monitor names will help your teams quickly identify what exactly is alerting and where. If we look above at our monitor setup we can see in the top portion of the screen
  our monitor name and the message that will be sent to the email specified. These can be as important as the alert itself as a poorly named monitor or poorly written message can be 
  as confusing as no monitoring at all.

## Monitor alert Email

- Now that our monitor is setup we will begin receiving email alerts whenever our sample is above 0.90. We can see one below.

![Alert_Email](screenshots/Alert_Email.png)


## Bonus: Set scheduled downtime for monitor, make sure Email is notified

- Finally, we would not want to be bothered at 2am for an alert that is going off because of a scheduled maintenance. We can schedule downtime for our alerts when we know there is maintenance
  happening. We can schedule downtime by going to **Monitors -> Manage Downtime** and setting the length of time for a particlar monitor. This can be set to email a specified person or team like below.

![Downtime_Email](screenshots/Downtime_Email.png)

# Conclusion

- Having worked with datadog before I knew it was a great product, I'm glad to see that it has continued to add features and grow within the monitoring scene. Also, because I've used datadog before
  this was not extremely technically challenging but I love that this is the way the company interviews a candidate. I believe it really lets you as a potential employee and datadog as a company 
  see how a person works and figures out problems hands on.
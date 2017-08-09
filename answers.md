# Datadog Solutions Engineer Exercise
A technical exercise for the Solutions Engineering interview process at Datadog.

Monitoring all of your applications and services, whether on-premises or in the cloud is a difficult task.  Each component has the potential of generating hundreds or thousands of events and metrics, and this only increases as your infrastructure scales to meet growing demands. You have to be able to correlate the datapoints from a wide variety of sources in order to get the full picture. Datadog solves this problem by letting you see everything in one place, in an intelligent and easily consumable format.

Datadog offers a myriad of easy to configure integrations from data sources such as:

- Cloud Providers
- Message Queues
- Code Repositories
- Cluster Tools
- Web Servers
- Monitoring Solutions
- Databases
- Operation Systems

...and more.

See https://www.datadoghq.com/ for **your** full story.

## Table of Contents

- [Setup an AWS EC2 Instance using a Linux AMI (Amazon Machine Image)](#setup-an-aws-ec2-instance-using-a-linux-ami-amazon-machine-image)
  - [Pre-requisites](#pre-requisites)
  - [Create Instance](#create-instance)
- [Collecting Your Data](#collecting-your-data)
  - [**Bonus Question: What is the Agent?**](#bonus-question-what-is-the-agent)
  - [Installing the Agent on AWS Linux AMI](#installing-the-agent-on-aws-linux-ami)
  - [Tagging](#tagging)
    - [AWS Integration](#aws-integration)
- [Create a MySQL instance](#create-a-mysql-instance)
  - [Create simple PHP webpage that connects to database](#create-simple-php-webpage-that-connects-to-database)
  - [Writing a Custom Agent Check](#writing-a-custom-agent-check)
- [Visualizing Data](#visualizing-data)
  - [MySQL Dashboard](#mysql-dashboard)
  - [Snapshot and Annotation](#snapshot-and-annotation)
- [Alerting on Data](#alerting-on-data)
  - [Create a Monitor](#create-a-monitor)
  - [Email Screenshot](#email-screenshot)
- [Conclusion](#conclusion)

## Setup an AWS EC2 Instance using a Linux AMI (Amazon Machine Image)
You can fairly easily set up your own free AWS EC2 instance by following these step-by-step instructions (~10 min):
### Pre-requisites
- Set up a free trial account at [https://aws.amazon.com/free/](https://aws.amazon.com/free/)
- You will need access to an SSH terminal
    - On Mac: use **Terminal**
    - On Windows: use **Putty** and **Putty Keygen**  
[https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
### Create Instance
- Log in to your AWS Management Console at [https://aws.amazon.com/console/](https://aws.amazon.com/console/)
- From the **Console Home** page, select **EC2** under "Compute":  
![Image](https://user-images.githubusercontent.com/30754481/29040773-e9cf5e22-7b75-11e7-8280-0c3a8edacb94.png)
- Select **Instances** from the left-hand navigation bar:  
![Image](https://user-images.githubusercontent.com/30754481/29040800-03b08a28-7b76-11e7-8c9c-23dd6d0d7dc2.png)
- Select [**Launch Instance**]:  
![Image](https://user-images.githubusercontent.com/30754481/29040815-12bfaa1c-7b76-11e7-91c8-2809c7eb7a51.png)  
- Select **Amazon Linux AMI**:  
![Image](https://user-images.githubusercontent.com/30754481/29040834-250e336e-7b76-11e7-92ab-480eecaed446.png)
- Select **t2.micro** instance type (to stay within free tier), then select [**Next: Configure Instance Details**]:  
![Image](https://user-images.githubusercontent.com/30754481/29040851-3721bb16-7b76-11e7-88bf-76858f395206.png)
- Leave all defaults and select [**Next: Add Storage**]:  
![Image](https://user-images.githubusercontent.com/30754481/29040866-45eba404-7b76-11e7-8902-5f29aa42a181.png)
- Leave all defaults and select [**Next: Add Tags**]:  
![Image](https://user-images.githubusercontent.com/30754481/29040882-5ae3d9c6-7b76-11e7-8fb0-40085122c8e1.png)
- Select [**Add Tag**] and enter:
    - Key: **Name**
    - Value: **DatadogWebServer**
    - Select [**Next: Configure Security Group**]
![Image](https://user-images.githubusercontent.com/30754481/29040902-68540004-7b76-11e7-97a6-a18683f8bfd4.png)
- **Configure Security Group** page:
    - (1) Choose "Create a **new** security group"
    - (2) Security group name: **MyWebDMZ**
    - (3) Description: **MyWebDMZ**
    - (4) Select [**Add Rule**]
    - (5) Type: **HTTP**
    - (6) Select [**Review and Launch**]:
![Image](https://user-images.githubusercontent.com/30754481/29044613-d823fe7a-7b85-11e7-8ee1-4aa92f61717a.png)
- Select [**Launch**]:  
![Image](https://user-images.githubusercontent.com/30754481/29040927-82a15ff6-7b76-11e7-8723-1ea15cd8af2e.png)
- Select "Choose an existing key pair" **MyNVPuttyKey** (or "Create a new key pair", enter "Key pair name", then select [**Download Key Pair**] if necessary)
- Check the "I acknowledge..." box, then select [**Launch Instances**]  
![Image](https://user-images.githubusercontent.com/30754481/29040931-8dd84380-7b76-11e7-9d69-da572f86cc78.png)
- Select [**View Instances**]. When **Instance State** changes to **running**, copy the **IPv4 Public IP** address, and SSH into the EC2 instance using the public IP and the key pair generated above
    - Windows:
        - Use "PuTTY Key Generator" to translate .pem file created above to .ppk format.
        - Use "PuTTY" to SSH into EC2 instance
        - Go to "Connection &gt; SSH &gt; Auth" and enter path to .ppk file created above
        - Go to "Session" and enter "Host Name (or IP address)": **ec2-user@_publicIP_** (using "IPv4 Public IP" address copied above)
    - Mac:
        - From "Terminal" window, change to directory with key pair file
        - **chmod 400 KeyPairFile.pem**
        - **ssh ec2-user@_publicIP_ -i KeyPairFile.pem** (using "IPv4 Public IP" address copied above)
![Image](https://user-images.githubusercontent.com/30754481/29040965-b0b73a1e-7b76-11e7-9b01-45ebc95b6d45.png)
- From your SSH window, enter the following commands:
    - **sudo su**  (to elevate permissions to root)
    - **yum update -y** (to apply all updates to EC2 instance)

## Collecting Your Data

### **Bonus Question: What is the Agent?**

The Datadog agent is a small piece of software that is loaded on your hosts, which will collect system level metrics (like CPU, memory, disk, etc.), and sends them to Datadog for reporting and analysis.  It can also collect custom application metrics via a small statsd server built in to the agent (DogStatsD).

### Installing the Agent on AWS Linux AMI
Installing a Datadog agent is as easy as 1, 2, 3! (<1 min)

1. Choose your OS type:  
![Image](https://user-images.githubusercontent.com/30754481/29050454-a8724bca-7ba1-11e7-815c-b06e4ba33ed6.png)  

2. For Amazon Linux, copy and paste their installer command in your SSH session (you should have administrator permissions). This will install the YUM packages for the Datadog Agent:
```
DD_API_KEY=c2341ce4c3d18943f6ca2bced618e823 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)" 
```
3. Press enter!  Here is expected output for Amazon Linux:  
```
[root@ip-172-31-30-110 ec2-user]# DD_API_KEY=c2341ce4c3d18943f6ca2bced618e823 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"  
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current  
                                 Dload  Upload   Total   Spent    Left  Speed  
100  9911  100  9911    0     0  54278      0 --:--:-- --:--:-- --:--:-- 54456  

* Installing YUM sources for Datadog  

* Installing the Datadog Agent package  

Loaded plugins: priorities, update-motd, upgrade-helper  
Resolving Dependencies  
--> Running transaction check  
---> Package datadog-agent.x86_64 1:5.16.0-1 will be installed  
--> Finished Dependency Resolution  

Dependencies Resolved  

================================================================================  
 Package               Arch           Version             Repository       Size  
================================================================================  
Installing:  
 datadog-agent         x86_64         1:5.16.0-1          datadog          69 M  

Transaction Summary  
================================================================================  
Install  1 Package  

Total download size: 69 M  
Installed size: 69 M  
Downloading packages:  
warning: /var/cache/yum/x86_64/latest/datadog/packages/datadog-agent-5.16.0-1.x86_64.rpm: Header V3 DSA/SHA1 Signature, key ID 4172a230: NOKEY  
Public key for datadog-agent-5.16.0-1.x86_64.rpm is not installed  
Retrieving key from https://yum.datadoghq.com/DATADOG_RPM_KEY.public  
Importing GPG key 0x4172A230:  
 Userid     : "Datadog Packages &lt;package@datadoghq.com&gt;"  
 Fingerprint: 60a3 89a4 4a0c 32ba e3c0 3f0b 069b 56f5 4172 a230  
 From       : https://yum.datadoghq.com/DATADOG_RPM_KEY.public  
Retrieving key from https://yum.datadoghq.com/DATADOG_RPM_KEY_E09422B3.public  
Importing GPG key 0xE09422B3:  
 Userid     : "Datadog, Inc &lt;package@datadoghq.com&gt;"  
 Fingerprint: a4c0 b90d 7443 cf6e 4e8a a341 f106 8e14 e094 22b3  
 From       : https://yum.datadoghq.com/DATADOG_RPM_KEY_E09422B3.public  
Running transaction check  
Running transaction test  
Transaction test succeeded  
Running transaction  
  Installing : 1:datadog-agent-5.16.0-1.x86_64                              1/1  
Stopping Datadog Agent (using killproc on supervisord): [FAILED]  
/etc/dd-agent/datadog.conf not found. Exiting.  
  Verifying  : 1:datadog-agent-5.16.0-1.x86_64                              1/1  

Installed:  
  datadog-agent.x86_64 1:5.16.0-1  

Complete!  

* Adding your API key to the Agent configuration: /etc/dd-agent/datadog.conf  

* Starting the Agent...  

Stopping Datadog Agent (using killproc on supervisord):    [FAILED]  
Starting Datadog Agent (using supervisord):                [  OK  ]  

Your Agent has started up for the first time. We're currently verifying that  
data is being submitted. You should see your Agent show up in Datadog shortly  
at:  

    https://app.datadoghq.com/infrastructure  

Waiting for metrics.................................  

Your Agent is running and functioning properly. It will continue to run in the  
background and submit metrics to Datadog.  

If you ever want to stop the Agent, run:  

    sudo /etc/init.d/datadog-agent stop  

And to run it again run:  

    sudo /etc/init.d/datadog-agent start  

[root@ip-172-31-30-110 ec2-user]# 
```
**That's all there is to it!**
### Tagging
Tagging makes it easy to group and filter on related sets of metrics and infrastructure components so that you can rapidly get to the root cause of an issue.  Datadog provides four methods to assign tags:

- **Inherited from the integration** - This is most recommended and easiest method to assign tags. Just install the integration, and the most common tags are automatically assigned.
- **Configuration files** - All tags are defined in the yaml configuration files located in the /etc/dd-agent/conf.d/ directory on Linux (C:\ProgramData\Datadog\conf.d\ on Windows). You can also define tags for the overall agent in /etc/dd-agent/datadog.conf on Linux (C:\ProgramData\Datadog\datadog.conf on Windows). Tags are defined using **key:value** pairs (recommended), although simple values are also valid.
- **Using the UI** - This method lets you assign tag to host through the user interface, however not to the integrations.
- **Using the API** - As with the UI method above, this method lets you assign tag to host through an API, however not to the integrations.

For this exercise, the AWS Integration was installed as follows:
#### AWS Integration
Setting up the Datadog integration with Amazon Web Services requires configuring role delegation using AWS Identity Access Management.

- From the **Console Home** page, select **IAM** under "Security, Identity & Compliance":  
![Image](https://user-images.githubusercontent.com/30754481/29098273-2cef8d46-7c64-11e7-958c-076276769e7a.png)  

- Select **Policies** from the left-hand navigation bar:  
![Image](https://user-images.githubusercontent.com/30754481/29098284-44e1115e-7c64-11e7-806e-1992e536cbd2.png)  

- Select [**Create policy**]:  
![Image](https://user-images.githubusercontent.com/30754481/29098297-5fb0029c-7c64-11e7-86ab-01f00fe43c88.png)  

- [**Select**] "Create Your Own Policy":  
![Image](https://user-images.githubusercontent.com/30754481/29098312-7026c444-7c64-11e7-8119-128cea9cf73f.png)  

- On **Review Policy** screen:
    - Policy Name: **DatadogAWSIntegrationPolicy**
    - Description: **DatadogAWSIntegrationPolicy**
    - Policy Document: **_Copy and paste the text below_**
    - Select [**Create Policy**]:
![Image](https://user-images.githubusercontent.com/30754481/29098330-855c5734-7c64-11e7-8e24-f26a7644a6d2.png)
```
{  
  "Version": "2012-10-17",  
  "Statement": [  
    {  
      "Action": [  
        "autoscaling:Describe*",  
        "budgets:ViewBudget",  
        "cloudtrail:DescribeTrails",  
        "cloudtrail:GetTrailStatus",  
        "cloudwatch:Describe*",  
        "cloudwatch:Get*",  
        "cloudwatch:List*",  
        "codedeploy:List*",  
        "codedeploy:BatchGet*",  
        "dynamodb:list*",  
        "dynamodb:describe*",  
        "ec2:Describe*",  
        "ec2:Get*",  
        "ecs:Describe*",  
        "ecs:List*",  
        "elasticache:Describe*",  
        "elasticache:List*",  
        "elasticfilesystem:DescribeFileSystems",  
        "elasticfilesystem:DescribeTags",  
        "elasticloadbalancing:Describe*",  
        "elasticmapreduce:List*",  
        "elasticmapreduce:Describe*",  
        "es:ListTags",  
        "es:ListDomainNames",  
        "es:DescribeElasticsearchDomains",  
        "kinesis:List*",  
        "kinesis:Describe*",  
        "lambda:List*",  
        "logs:Get*",  
        "logs:Describe*",  
        "logs:FilterLogEvents",  
        "logs:TestMetricFilter",  
        "rds:Describe*",  
        "rds:List*",  
        "route53:List*",  
        "s3:GetBucketTagging",  
        "s3:ListAllMyBuckets",  
        "ses:Get*",  
        "sns:List*",  
        "sns:Publish",  
        "sqs:ListQueues",  
        "support:*",  
        "tag:getResources",  
        "tag:getTagKeys",  
        "tag:getTagValues"  
      ],  
      "Effect": "Allow",  
      "Resource": "*"  
    }  
  ]}
```

- Type first few letters of new policy name in the search field to confirm successful creation. Then select **Roles** from the left-hand navigation bar:  
![Image](https://user-images.githubusercontent.com/30754481/29098339-92a39100-7c64-11e7-961d-9a8ef0a495f6.png)  

- Select [**Create new role**]:  
![Image](https://user-images.githubusercontent.com/30754481/29098349-9ff46442-7c64-11e7-8e5b-7ba6d1e67a9d.png)  

- Choose **Role for cross-account access**, then [**Select**] **Provide access between your AWS account and a 3rd party AWS account**:  
![Image](https://user-images.githubusercontent.com/30754481/29098395-cc180e48-7c64-11e7-837e-e8982ef1008b.png)  

- On the next screen, enter the following:
    - Account ID: **464622532012**
    - External ID: _**Generated from Datadog website**_
    - Require MFA: **_Leave unchecked_**
    - Select [**Next Step**]  
![Image](https://user-images.githubusercontent.com/30754481/29098408-dbd8f284-7c64-11e7-93da-a2e5ad9e7de3.png)  

- Select the **DatadogAWSIntegrationPolicy** created above, then select [**Next Step**]:  
![Image](https://user-images.githubusercontent.com/30754481/29098422-ea80ce56-7c64-11e7-817a-9e9e39a1ba4d.png)  

- On **Set role name and review** screen:
    - Role name: **DatadogAWSIntegrationRole**
    - Role description: **DatadogAWSIntegrationRole**
    - Select [**Create role**]  
![Image](https://user-images.githubusercontent.com/30754481/29098431-f77eaac4-7c64-11e7-8ffe-de798b2f282a.png)  

- From the Datadog console, open the AWS Integration tile ([https://app.datadoghq.com/account/settings#integrations/amazon_web_services](https://app.datadoghq.com/account/settings#integrations/amazon_web_services))
    - (1) Select the **Role Delegation** tab
    - (2) Enter your **AWS Account ID** without dashes. Your Account ID can be found in the ARN of the newly created role.
    - (3) Enter **AWS Role name** you just created.
    - (4) Enter the **AWS External ID** you specified above.
    - (5) Choose the **AWS Service**s you want to collect metrics for on the left side of the dialog.  
![Image](https://user-images.githubusercontent.com/30754481/29098446-05c25518-7c65-11e7-988f-70f095ba4d0f.png)
    - Select [**Install Integration**]:  
![Image](https://user-images.githubusercontent.com/30754481/29098454-12e00452-7c65-11e7-91c7-f7bea3404d4c.png)  

- **AWS specific tags are automatically assigned!**
![Image](https://user-images.githubusercontent.com/30754481/29098467-1eac3210-7c65-11e7-87be-cefcdbcff8e6.png)

- Tags can also be added to **/etc/dd-agent/datadog.conf** as follows:
```
# Set the host's tags (optional)  
# tags: mytag, env:prod, role:database  
tags: name:king_arthur, quest:seek_holy_grail, fav_color:blue
```
![Image](https://user-images.githubusercontent.com/30754481/29100965-c80ce26e-7c74-11e7-9b94-c5fd918c9f13.png)

## Create a **MySQL** instance

- From the **Console Home** page, select **RDS** under "Database":  
![Image](https://user-images.githubusercontent.com/30754481/29035490-677d754e-7b61-11e7-9916-6a8da69fabf2.png)
- Select **Instances** from left-hand navigation bar:  
![Image](https://user-images.githubusercontent.com/30754481/29035597-cb71219a-7b61-11e7-8b8c-37e57c8cc174.png)
- Select [**Launch DB Instance**]  
![Image](https://user-images.githubusercontent.com/30754481/29035610-d6313f7a-7b61-11e7-91c1-acae92184a6b.png)
- Choose **MySQL** tab and select [Select]  
![Image](https://user-images.githubusercontent.com/30754481/29035615-dbda0128-7b61-11e7-8e9c-f40b73475152.png)
- Select **Dev/Test** MySQL (to stay in RDS Free Usage Tier), then select [**Next Step**]  
![Image](https://user-images.githubusercontent.com/30754481/29035618-df974244-7b61-11e7-9fe3-d8757db82811.png)
- **Specify DB Details** page:
![Image](https://user-images.githubusercontent.com/30754481/29036979-44d26760-7b67-11e7-8a66-673e91cbb030.png)
    - (1) DB Instance Class: **db.t2.micro** (to stay within free tier)
    - (2) Multi-AZ Deployment: **No** (also for free tier)
    - (3) Enter "DB Instance Identifier": **iluvdatadog**
    - (4) Enter "Master Username": **iluvdatadog**
    - (5) Enter "Master Password": ************
    - (6) Enter "Confirm Password": ************
    - (7) Select [Next Step]

**NOTE: Keeping DB Name and Username the same for ease of administration during this exercise only.  This is not best practice for a production environment.**
- **Configure Advanced Settings** page:
![Image](https://user-images.githubusercontent.com/30754481/29037812-de7cefc2-7b6a-11e7-81c4-94fa12b652ac.png)
    - (1) Confirm "VPC" is **Default VPC**
    - (2) Select "Publicly Accessible": **No**
    - (3) Select "VPC Security Group(s)": **Create new Security Group**
    - (4) Enter "Database Name": **iluvdatadog**
    - (5) Select [Launch DB Instance]
- Select [**View Your DB Instances**]  
![Image](https://user-images.githubusercontent.com/30754481/29035631-eb7e52e6-7b61-11e7-8bbf-3eef92f63bbb.png)
- Select "Details" tab, then select link beside **Security Groups**:  
![Image](https://user-images.githubusercontent.com/30754481/29035636-eed51920-7b61-11e7-86ca-31eb61274a55.png)
- Select **Inbound** rule tab of **rds-launch-wizard** group, then select [**Edit**]  
![Image](https://user-images.githubusercontent.com/30754481/29039097-88670f14-7b6f-11e7-9190-b335eea685fb.png)
- **Edit inbound rules** page:
    - Change the **Source** from the public IP to the security group **MyWebDMZ** that you created with the EC2 instance (you can type "**s**" to see a list of available security groups).
    - Select [**Save**]
![Image](https://user-images.githubusercontent.com/30754481/29039104-92c14a74-7b6f-11e7-86d7-f17cdc71a158.png)
**NOTE**: This is to allow traffic in from web server on port 3306 (MySQL) so it can communicate with database.
### Create simple PHP webpage that connects to database
- From the RDS Dashboard in the AWS Console, select the MySQL database you created above, and copy the database Endpoint address to your clipboard buffer:  
![Image](https://user-images.githubusercontent.com/30754481/29040990-c70c0d94-7b76-11e7-8f14-060304cfe7a1.png)
- From your SSH window, enter the following commands:
    - **sudo su**  (to elevate permissions to root)
    - **yum update -y** (to apply all updates to EC2 instance)
    - **yum install httpd php php-mysql -y** (to install Apache, PHP, and PHP-MySQL)
    - **service httpd start** (to start Apache service)
    - **chkconfig httpd on** (to start Apache service automatically on re-boot)
    - **echo "&lt;?php phpinfo();?&gt;" &gt; /var/www/html/index.php** (to create simple PHP webpage)
    - **cd /var/www/html**  (to change to Apache directory)
    - **nano connect.php** (to create the following PHP script to connect to MySQL database):
```php
&lt;?php
$username = "iluvdatadog";
$password = "*********";
$hostname = "iluvdatadog.c2zwfrvpwfuo.us-east-1.rds.amazonaws.com:3306";
$dbname = "iluvdatadog";

//connection to the database
$dbhandle = mysql_connect($hostname, $username, $password) or die("Unable to connect to MySQL");
echo "Connected to MySQL using username - $username, host - $hostname&lt;br&gt;";
$selected = mysql_select_db("$dbname",$dbhandle)   or die("Unable to connect to MySQL DB - check the database name and try again.");
?&gt;
```

**NOTE**:  The **$hostname** value is from the database endpoint copied above.

### Writing a Custom Agent Check

## Visualizing Data
### MySQL Dashboard
### Snapshot and Annotation

## Alerting on Data
### Create a Monitor
### Email Screenshot

## Conclusion

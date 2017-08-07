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
  - [Installing the Agent on AWS Linux AMI](#installing-the-agent-on-aws-linux-ami)
  - [Tagging](#tagging)
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
You can fairly easily set up your own AWS EC2 instance by following these step-by-step instructions:
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

**Bonus Question: What is the Agent?**

The Datadog agent is a small piece of software that is loaded on your hosts, which will collect system level metrics (like CPU, memory, disk, etc.), and sends them to Datadog for reporting and analysis.  It can also collect custom application metrics via a small statsd server built in to the agent (DogStatsD).

### Installing the Agent on AWS Linux AMI

### Tagging

## Create a **MySQL** instance

- From the **Console Home** page, Select **RDS** under "Database":  
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

**Bonus Question: What is the Agent?**

The Datadog agent is a small piece of software that is loaded on your hosts, which will collect system level metrics (like CPU, memory, disk, etc.), and sends them to Datadog for reporting and analysis.  It can also collect custom application metrics via a small statsd server built in to the agent (DogStatsD).

Setup an AWS EC2 Instance using a Linux AMI (Amazon Machine Image)

- Set up a free trial account at [https://aws.amazon.com/free/](https://aws.amazon.com/free/)
- You will need access to an SSH terminal
    - On Mac: use **Terminal**
    - On Windows: use **Putty** and **Putty Keygen**  
[https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

- Log in to your AWS Management Console at [https://aws.amazon.com/console/](https://aws.amazon.com/console/)
- Create a **MySQL** instance
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

          1. DB Instance Class: **db.t2.micro** (to stay within free tier)
          2. Multi-AZ Deployment: **No** (also for free tier)
          3. Enter "DB Instance Identifier": **iluvdatadog**
          4. Enter "Master Username": **iluvdatadog**
          5. Enter "Master Password": ************
          6. Enter "Confirm Password": ************
          7. Select [Next Step]

**NOTE: Keeping DB Name and Username the same for ease of administration during this exercise only.  This is not best practice for a production environment.**
    - **Configure Advanced Settings** page:
![Image](https://user-images.githubusercontent.com/30754481/29035624-e7289170-7b61-11e7-810d-7cf91fab4858.png)
        - Confirm "VPC" is **Default VPC**
        - Select "Publicly Accessible": **No**
        - Select "VPC Security Group(s)": **Create new Security Group**
        - Enter "Database Name": **iluvdatadog**
        - Select [Launch DB Instance]
    - Select [**View Your DB Instances**]  
![Image](https://user-images.githubusercontent.com/30754481/29035631-eb7e52e6-7b61-11e7-8bbf-3eef92f63bbb.png)
    - Select "Details" tab, then select link beside **Security Groups**:  
![Image](https://user-images.githubusercontent.com/30754481/29035636-eed51920-7b61-11e7-86ca-31eb61274a55.png)
    - Select [**Create Security Group**]:   
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(144).png)
    - **Create Security Group** page:
    - 
        - Security group name: **MyWebDMZ**
        - Description: **MyWebDMZ**
        - VPC: leave as **default**
        - **Inbound** rule tab -- [**Add Rule**]
        - 
            - Type: **HTTP**; Source: **0.0.0.0/0, ::/0**
            - Type: **SSH**; Source: **0.0.0.0/0, ::/0**

        - Select [**Create**]

- 
    - Select **Inbound** rule tab of **rds-launch-wizard** group, then select [**Edit**]  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(146).png)
    - **Edit inbound rules** page:
    - 
        - Change the **Source** from the public IP to the security group you just created (you can type "**s**" to see a list of available security groups).
        - Select [**Save**]

**NOTE**: This is to allow traffic in from web server on port 3306 (MySQL) so it can communicate with database.

- Create EC2 instance and simple PHP webpage
- 
    - From the **Console Home** page, select **EC2** under "Compute":  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(148).png)
    - Select **Instances** from the left-hand navigation bar:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(149).png)
    - Select [**Launch Instance**]:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(150).png)  

    - Select **Amazon Linux AMI**:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(151).png)
    - Select **t2.micro** instance type (to stay within free tier), then select [**Next: Configure Instance Details**]:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(152).png)
    - Leave all defaults and select [**Next: Add Storage**]:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(153).png)
    - Leave all defaults and select [**Next: Add Tags**]:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(154).png)
    - Select [**Add Tag**] and enter:
    - 
        - Key: **Name**
        - Value: **DatadogWebServer**
        - Select [**Next: Configure Security Group**]

- 
    - Choose "Select an **existing** security group", select **MyWebDMZ**, then select [**Review and Launch**]:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(156).png)
    - Select [**Launch**]:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(157).png)
    - Select "Choose an existing key pair" **MyNVPuttyKey** (or "Create a new key pair", enter "Key pair name", then select [Download Key Pair] if necessary)
    - Check the "I acknowledge..." box, then select [Launch Instances]  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(158).png)
    - Select [**View Instances**]. When **Instance State** changes to **running**, copy the **IPv4 Public IP** address, and SSH into the EC2 instance using the public IP and the key pair generated above
    - 
        - Windows:
        - 
            - Use "PuTTY Key Generator" to translate .pem file created above to .ppk format.
            - Use "PuTTY" to SSH into EC2 instance
            - Go to "Connection &gt; SSH &gt; Auth" and enter path to .ppk file created above
            - Go to "Session" and enter "Host Name (or IP address)": **ec2-user@_publicIP_** (using "IPv4 Public IP" address copied above)

        - Mac:
        - 
            - From "Terminal" window, change to directory with key pair file
            - **chmod 400 KeyPairFile.pem**
            - **ssh ec2-user@_publicIP_ -i KeyPairFile.pem** (using "IPv4 Public IP" address copied above)

- 
    - From the RDS Dashboard in the AWS Console, select the MySQL database you created above, and copy the database Endpoint address to your clipboard buffer:  
![Image](file:///C:/Users/dbeal/Evernote/TEMP/enhtmlclip/Image(160).png)
    - From your SSH window, enter the following commands:
    - 
        - **sudo su**  (to elevate permissions to root)
        - **yum update -y** (to apply all updates to EC2 instance)
        - **yum install httpd php php-mysql -y** (to install Apache, PHP, and PHP-MySQL)
        - **service httpd start** (to start Apache service)
        - **chkconfig httpd on** (to start Apache service automatically on re-boot)
        - **echo "&lt;?php phpinfo();?&gt;" &gt; /var/www/html/index.php** (to create simple PHP webpage)
        - **cd /var/www/html**  (to change to Apache directory)
        - **nano connect.php** (to create the following PHP script to connect to MySQL database):

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

- 
    - 
        - **NOTE**:  The **$hostname** value is from the database endpoint copied above.

### Here are my answers to the technical exercise

## Setup:
* My Environment:
  * Ubuntu VM - Vagrant setup / VirtualBox
  * Installed the Agent via the curl command per instructions
    * Error: The program 'curl' is currently not installed.
    * Installed curl: <b>sudo apt-get install curl</b>
  * Installed and started MySQL Server on the VM
  
## Collecting Metrics:
* Created tags for the this host by editing the /etc/datadog-agent/datadog.yaml
  <img src=screenshots/datadog.yaml.jpg>
 
* Restarted the Agent: <B>sudo service datadog-agent restart</B>
* Verified new tag shows in Host Map view
  <img src=screenshots/hostmap.jpg>

* MySql Integration Setup
  * Instructions on configuration @ https://app.datadoghq.com/account/settings#integrations/mysql
  * datadog-agent status - error result on mysql config:
    <img src=screenshots/mysql_error.png>
  * Fixed issue with formating of conf.yaml file (space indentation):
    <img src=screenshots/conf.yaml.jpg>
  * datadog-agent status - warning result on mysql config:
    <img src=screenshots/mysql_warning.png>
    * Researched warning message:  <I>Warning: Privilege error or engine unavailable accessing the INNODB status</I>
    * Found: https://github.com/DataDog/dd-agent/issues/2376
    * Re-executed following and fixed the warning (thought I already did, but tried again :-)
       * sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
       * sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
  * datadog-agent status - now OK  (woo hoo!)
    <img src=screenshots/mysql_good.png>

        
      



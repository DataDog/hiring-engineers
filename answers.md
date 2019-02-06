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


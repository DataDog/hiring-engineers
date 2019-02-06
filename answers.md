### Here are my answers to the technical exercise

## Setup:
* My Environment:
  * VM - Ubuntu 12.04 - Vagrant setup / VirtualBox
  * Installed the Agent via the curl command per instructions
    * Error: The program 'curl' is currently not installed.
    * Installed curl: <b>sudo apt-get install curl</b>
  * Installed and started MySQL Server on the VM
  
## Collecting Metrics:
* Created tags for the this host by editing the /etc/datadog-agent/datadog.yaml
* restarted the Agent via systemctl
* Below is a screen shot showing my new host tags via the Host Map Page:

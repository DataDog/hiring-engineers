Pre-Requisites / Setup

Having never used Vagrant, I thought I’d give this a go as it’s something new to learn about! 

•	Create Host for exercise - Ubuntu Server Installed on MacOS (Vagrant and VirtualBox)
    o	Renamed VM from “vagrant” to “lukeDD”
    
•	Signed up to DataDog (email@lukelim.com)

•	Installed Datadog Ubuntu agent on my VM
    o	My Agent Install Command: DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=5b21cddf0e509ced5358c8bb2c57c97d DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
    
•	Successful agent Install and DataDog shows it installed: ![](images/Setup.png)

•	Then I had a good click around the system! 

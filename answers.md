Pre-Requisites / Setup

Having never used Vagrant, I thought I’d give this a go as it’s something new to learn about! 

•	Create Host for exercise - Ubuntu Server Installed on MacOS (Vagrant and VirtualBox)
    
    o	Renamed VM from “vagrant” to “lukeDD”
    
•	Signed up to DataDog (email@lukelim.com)

•	Installed Datadog Ubuntu agent on my VM
    
    o	My Agent Install Command: DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=5b21cddf0e509ced5358c8bb2c57c97d DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
    
•	Successful agent Install and DataDog shows it installed: ![](images/Setup.png)

•	Then I had a good click around the system! 


Collection Metrics

Had a browse through the options in the datadog.yaml file and realise there are a lot of options and all very well documented both in the yaml file itself and the product documentation! This gives and very good and starting point for a Datadog user to take up the basics and configure further.

Tags – Tags area great thing for a data platform and monitoring system as one of the biggest challenges in the data is understanding context and versioning for long term data validity. Tags allow this by making sure the data is grouped correctly for my business/team’s needs and also helps if we tag a transient metric or datapoint in case the underlying infrastructure is dynamic. Ie. A service moves and changes spec but it’s use and therefore reporting remains the same… I want to ensure this is reflected in my reports/dashboards/alerts.

Q. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Didn’t want to go crazy with this but set up a few tags to see how they’d be reflected in the UI.

# Solutions Engineer Exercise

## Setup
For this open source exercise I'm running Ubuntu 16.04 on my device. Before installing the agent, I read through the documentation located at the bottom of the assignment in order to gain an understanding of the Datadog agent.  

Download the Datadog Agent in terminal.
```
DD_API_KEY=f3a6ab39d4e712b846b54ad0ccaa2083 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
<img src="https://github.com/alexandera9996/hiring-engineers/blob/master/datadog_screenshots/agent_ok.png" />


## Collecting Metrics
Tagging gives the user a method of aggregating data across a number of hosts. This is useful because users can then compare and observe how metrics behave across a number of hosts or collection of systems. 
navigate to Datadog directory

```
cd /etc/datadog-agent
```
Open Datadog.yaml:
```
sudo vim Datadog.yaml
```
Configure your .yaml file and change the tags to your preference. These are my tags:
(insert tag.png photo)

Restart the agent:
```
sudo service datadog-agent restart
```
Navigate to Host Map page in Data dog. Reload the page if your new tags do not appear.
Here is my Host Page map for reference.
(insert Host_page.png)

### Install a database. For this part, I went ahead with MongoDB

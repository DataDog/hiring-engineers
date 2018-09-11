# Solutions Engineer Exercise

## Setup
For this open source exercise I'm running Ubuntu 16.04 on my device. 

Download the Datadog Agent in terminal.
```
DD_API_KEY=f3a6ab39d4e712b846b54ad0ccaa2083 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```


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

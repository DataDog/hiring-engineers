# DataDog Tech Assessment Sales Engineer
Andrew Hartzell

## Set up the Environment

Already have a version of Ubuntu installed on VirtualBox - will use that for this test.

**Install the DD agent**

<img src="/screenshots/dd_agent_install.png" alt="Ubuntu up and running" style="height: 125px; width:300px;"/>

**Appears in dashboard**
<img src="/screenshots/dd_dash.png" alt="Ubuntu up and running" style="height: 125px; width:300px;"/>

## Collecting Metrics

**Add tags in config file - host + tags on host map page in DD**

cd /etc/datadog-agent/
nano datadog.yaml (add tags)

**Restart Agent so updated tags will appear in dash**
sudo systemctl restart datadog-agent.service

<img src="/screenshots/hostmap_tags.png" alt="Ubuntu up and running" style="height: 150px; width:400px;"/>
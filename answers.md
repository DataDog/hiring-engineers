Your answers to the questions go here.
# Level 0 Answer "setup an ubuntu VM"

I have used my Mac, and I already have a CentOS VM which I think is running a database.

# Level 1 

## Sign up for DataDog

I signed up for DataDog a week ago (mark@jeffery.com), and I have changed the company name to Datadog Recruiting Candidate

## Bonus Question: What is an agent

The datadog agent is some software that runs in the background on a computer, and measures metrics and events, sending them up the DataDog SaaS servers. The agent collects standard Infrastructure metrics (CPU utilisation etc), but it is also able to collect metrics from Cloud providers (AWS, Azure etc), Databases (MySQL, MongoDB etc), Web Servers (IIS, Apache etc) and container technologies (Docker, Kubernetes etc)

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Edited /etc/dd-agent/datadog.conf

Added some tags to define the server

![definition of tags](https://github.com/markjeffery/hiring-engineers/blob/master/screen%20shot%20-%20tag%20definition.png)

Restarted agent (not sure if I needed to)

Checked out the infrastructure menu, selected my new server in the host map, and clicked on system. It shows the tags.

![tags shown in datadog](https://github.com/markjeffery/hiring-engineers/blob/master/screen%20shot%20-%20tag%20results.png)


TASK #2: Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

ANSWER #2:

Brief Explanation:
I signed up to Datadog.com and get the download link for datadog agent.
DD_API_KEY=32f8a12f62e1275f6369ffc379b1ee82 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
I used both one-step install and step-by-step installn on my 2 VMs

Steps:
- Login to my VM boxes
- Run the script, this is the brief output:

root@sg-web-01:~# DD_API_KEY=32f8a12f62e1275f6369ffc379b1ee82 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog                                                                                                           -agent/master/cmd/agent/install_script.sh)"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 11382  100 11382    0     0  14941      0 --:--:-- --:--:-- --:--:-- 14937
* Installing apt-transport-https
* Installing the Datadog Agent package
* Adding your API key to the Agent configuration: /etc/datadog-agent/datadog.yaml
* Starting the Agent...
Your Agent is running and functioning properly. It will continue to run in the background and submit metrics to Datadog.
If you ever want to stop the Agent, run:
     systemctl stop datadog-agent
And to run it again run:
     systemctl start datadog-agent

Reference:
https://app.datadoghq.com/account/settings#agent/ubuntu

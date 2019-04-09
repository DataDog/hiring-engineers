## Environment Setup

Host OS: Mac OS X
Installed Vagrant
Vagrant OS: ubuntu/xenial64
  
  ## Collecting Metrics
  
##  Install Agent

```
  DD_API_KEY=<<API_KEY>> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

##  Adding Tags

The configuration files and folders for the Agent are located in:

/etc/datadog-agent/datadog.yaml

1. edit datadog.yaml
2. Add tags

```
tags:
    - env:trial
    - type:vagrant
    - role:dd_challenge
```
3. Host Map in action

![Host Map](/img/Host_Map.png)




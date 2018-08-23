## Setup the environment

-I used Mac OS X 10.13.6 for my environment, signed up for a trial account and installed the agent via terminal with the following command:

```DD_API_KEY=<api_key> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"```

## Collecting Metrics

-Added unique tags and aliased my host name by opening the `datadog.yaml` config file located in `/opt/datadog-agent/etc/`: 

![config file](https://imgur.com/mPHnEYF)

then checked to confirm the changes had taken effect in the host map:

![host map](https://imgur.com/FHhDMJc)

-Due to my familiarity and already having it installed on my machine, I decided on PostgreSQL as my database of choice. I completed [integration](https://imgur.com/mNgXPNE) by following the configuration steps found [here](https://app.datadoghq.com/account/settings#integrations/postgres) and editing the `postgres.yaml` [file](https://imgur.com/5HTZ4Sm) found in `/opt/datadog-agent/etc/conf.d`.

-Created custom check file `checkvalue.py` and it's corresponding config file `checkvalue.yaml` at 

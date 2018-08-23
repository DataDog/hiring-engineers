## Setup the environment

-I used Mac OS X 10.13.6 for my environment, signed up for a trial account and installed the agent via terminal with the following command:

```DD_API_KEY=<api_key> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"```

## Collecting Metrics

-Added unique tags and aliased my host name by opening the `datadog.yaml` [config file](https://imgur.com/mPHnEYF) located in `/opt/datadog-agent/etc/` then checked to confirm the changes had taken effect in the [Host Map](https://imgur.com/FHhDMJc).

-Due to being previously installed on my machine and my familiarity with it, I decided on PostgreSQL as my database of choice. I completed [integration](https://imgur.com/mNgXPNE) by following the configuration steps found [here](https://app.datadoghq.com/account/settings#integrations/postgres) and editing the `postgres.yaml` [file](https://imgur.com/5HTZ4Sm) found in `/opt/datadog-agent/etc/conf.d`. I then ran `datadog-agent status` in terminal to confirm my integration was successful by finding [this output](https://imgur.com/4gBQhtU).

-Created [custom check file](https://imgur.com/UOBaWEm) `checkvalue.py` and it's [corresponding config file](https://imgur.com/pdev577) `checkvalue.yaml` in `/opt/datadog-agent/etc/checks.d` and `/opt/datadog-agent/etc/conf.d`, respectively.

#### Bonus Question: Can you change the collection interval without modifying the Python check file you created?

If the question is referring specifically to the checkvalue.py file, then yes the interval can be changed via it's accompanying config file. However if the question is considering this pair of files as a singular check file, then I'm not aware of ways to accomplish this outside of these files.

## Visualizing Data

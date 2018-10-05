# Collecting Metrics

Configure the collection of basic and user-defined metrics from the VM.

### Adding tags in the Agent config file

1. Enter the Vagrant VM setup in [Section 0](./0_setting_the_environment.md) using the following command:
    ```
    $ vagrant ssh
    ```
2. Modify the Datadog Agent configuration **/etc/datadog-agent/datadog.yaml** as follows:
    ```
    # Set the host's tags (optional)
    
    tags:
      - hiring_challenge 
      - env:dev
      - role:database
    ```
    Checkout the [guide](https://docs.datadoghq.com/tagging/) to learn about the best practice in using tags.

3. Restart the Datadog Agent:
    ```
    $ sudo systemctl stop datadog-agent
    $ sudo systemctl start datadog-agent
    ```

4. Tags can be viewed by navigating the Datadog interface: Infrastructure > Host Map

    ![Alt text](../images/1_tags.png?raw=true "Viewing Tags")
    
### Installing PostgreSQL and its Datadog integration

1. Update the apt command, the install PostgreSQL:
    ```
    $ sudo apt-get update
    $ sudo apt-get install postgresql postgresql-contrib
    ```
2. Follow the Postgres Integration [instructions](https://app.datadoghq.com/account/settings#integrations/postgres). Note that you need to create the config file: /etc/datadog-agent/conf.d/postgres.d/postgres.yaml.

3.  Restart the Datadog Agent.

### Create a custom Agent check
Create a custom Agent check that submits a random value between 0 and 1000.

1. Create the file /etc/datadog-agent/checks.d/check.py:
    ```
    import random
    from checks import AgentCheck
    
    class MyCheck(AgentCheck):
        def check(self, instance):
            self.gauge('my_check', random.randint(0, 1000))
    ```
2. Create the file /etc/datadog-agent/conf.d/check.d/check.yaml:
    ```
    init_config:
    
    instances:
        [{}]
    ```
3. Custom metric can be viewed by navigating the Datadog interface: Metrics

    ![Alt text](../images/1_custom_metric.png?raw=true "Custom Metric")

### Modifying custom check's collection interval
Change the check's collection interval so that it only submits the metric once every 45 seconds. This can be done without modifying the /etc/datadog-agent/checks.d/check.py.

1. Modify the file /etc/datadog-agent/conf.d/check.d/check.yaml:
    ```
    init_config:
        min_collection_interval: 45
    instances:
        [{}]
    ```



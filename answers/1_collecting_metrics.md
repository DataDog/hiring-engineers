### Collecting Metrics

Configure the collection of basic and user-defined metrics from the VM.

###### Adding tags in the Agent config file

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

3. Restart the Datadog Agent using the following commands:
    ```
    $ sudo systemctl stop datadog-agent
    $ sudo systemctl start datadog-agent
    ```

4. Tags can be viewed by navigating the Datadog interface: Infrastructure > Host Map

![Alt text](./images/1_tags?raw=true "Viewing Tags")
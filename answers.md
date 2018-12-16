Your answers to the questions go here.


### Part 1: Collecting Metrics:

1. _Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog._


__Tag Setup__:

* Create agent by running command provided in 1-setup

* Once the agent has been created, start a Docker container Bash session with command

  ```bash
  docker exec -it dd-agent /bin/bash
   ```


* Access and update agent config file (`datadog.yaml`) from terminal by running the following command:

  ```bash
  vim /etc/datadog-agent/datadog.yaml
  ```


* Once you see the file contents in your terminal, press `i` (for "insert") and add tag list to `datadog.yaml`:


  <a href='./images/1.01-datadog.yaml-tag-screenshot.jpeg'><img src="Images/1.01-datadog.yaml-tag-screenshot.jpeg" width="500" height="332" alt="datadog.yaml-tag-code"></a>


  * When you're satisfied with your updates to `datadog.yaml`, press `esc` to exit vim's edit mode, and type `:wq` to exit from vim

  * End the docker container bash session by running `exit`

  * Restart your Datadog agent with the following command:

  ```bash

  ```

  * Navigate to Host Map in your Datadog Dashboard and you should see the new tags listed:

  <a href='./images/1.01-datadog.yaml-tag-screenshot.jpeg'><img src="images/1.01-dashboard-tag-screenshot.jpeg" width="500" alt="datadog.yaml-tag-code"></a>





2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

4. Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?

### Level 1 - Collecting Data

* TASK: Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the Agent reporting metrics from your local machine.
  - [Link to Host Dashboard](https://app.datadoghq.com/dash/host/349301929?live=true&page=0&is_auto=false&from_ts=1507061300792&to_ts=1507064900792&tile_size=m)
  - This image shows initial metrics gathered from a virtual Linux system by the Datadog agent:
  <br><br>
  ![Initial Host Dashboard After Setup](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/initial_host_dashboard.JPG?raw=true)


* BONUS QUESTION: In your own words, what is the Agent?
  - The agent is software installed to run on a host and collect events and metrics about an application or overall infrastructure.
  - It is composed of three main parts each with different tasks.
    - The collector captures system metrics like memory and CPU usage from the current machine and/or the host integrations.
    - To send custom metrics from an application the agent uses a statsd backend server called Dogstatsd
    - The forwarder interacts with the collector and Dogstatsd to retrieve data from both and queue it for transfer to Datadog.
  - Click [here](https://docs.datadoghq.com/guides/basic_agent_usage/) for more information and a full description of the Datadog Agent.


* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  - Here is a screenshot of the Agent config file (datadog.conf), opened with the built in Nano editor, showing two custom tags added (on a line near the middle of the image):
  <br><br>
  ![Custom tags in Agent config file.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/dd_agent_config_tags.JPG?raw=true)

  - This is an image of the Host Map page displaying the tags entered on the datadog.conf file:
  <br><br>
  ![Host Map page screenshot with tags displayed.](https://github.com/MikeTarkington/hiring-engineers/blob/support-engineer/initial_host_map_tags.JPG?raw=true)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
* Write a custom Agent check that samples a random value. Call this new metric: `test.support.random`

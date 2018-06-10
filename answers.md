Sarah Schaab - Solutions Engineer Candidate

Setup:
I set up my environment with Vagrant and VirtualBox.
I then installed the Datadog Agent for Mac OSX using the command line and the Datadog Agent Install instructions.


Collecting Metrics:

  Adding Host Tags

    After a bit of experimentation working with the datadog.yaml file and the datadog UI Dashboard I found the documentation for assigning Tags at https://docs.datadoghq.com/getting_started/tagging/assigning_tags/
    First, I chose to add a tag through the UI, with a key of hello and a value of world "hello:world"
    Then, I navigated to the datadog.yaml file and uncommented line 35, "tags:", and added my own tags, region:eastus, region:westus, and region:centralus.

    According to the documentation you should use the following form in the datadog.yaml file:
    tags: key_first_tag:value_1, key_second_tag:value_2, key_third_tag:value_3

    Upon trying to restart the agent, I ran into an error and went with the second form listed:
    tags:
      - key_first_tag:value_1
      - key_second_tag:value_2
      - key_third_tag:value_3

   Installing DB and DB integration

      I am using MongoDB, I already have it installed on my machine so I am skipping the installation process.

      Navigating to the conf.d/Mongo.d file I created a file called Mongo.yaml
      and added the recommended config file from the Datadog documentation.
      source: https://github.com/DataDog/integrations-core/blob/master/mongo/conf.yaml.example

      In the Mongo shell I created a user 'datadog' within my admin db.
      following the steps provided in the documentation
        db.createUser({
            "user":"datadog",
            "pwd": "<UNIQUEPASSWORD>",
            "roles" : [
              {role: 'read', db: 'admin' },
              {role: 'clusterMonitor', db: 'admin'},
              {role: 'read', db: 'local' }
            ]
          })

      In the mongo.yaml file I changed the server to
      - server: mongodb://datadog:<myPassword>@127.0.0.1/admin

      In the Datadog Dashboard I navigated to the integrations tab and downloaded the Mongodb Integration.

      I restarted the agent and saw that there was an error with the mongo check connecting to port 27017.
      I removed the .lock file from MongoDB, and still ran into this error.

      In the Mongo Dashboard I have available 1 available hosts, but in the checks summary I am recieving 7 critical warnings under the mongodb.can_connect check.

      I stopped the agent and ran
      - echo "db.auth('datadog', 'ddsolutions')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" && echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"

      When I recieved the output:
      exception: connect failed
      datadog user - OK

      I tried multiple solutions, but continuously ran into this issue. I believe it is an issue with my machine's version of MongoDB.

      I initially installed MongoDB using Homebrew, so I uninstalled it running "brew uninstall mongo"

      Upon trying to reinstall MongoDB, I found that it's dependency on Python was crashing the install process. In terminal "which python" was resulting in "/Library/Frameworks/Python.framework/Versions/2.7/bin/python" I knew this was an error, because it should be located in /usr/local/bin/python.

      These are the steps that I took to solve the issue:
        - nano .bashrc
      In Bash I added the line: export PATH=/usr/local/bin:$PATH
      saved Bash, and exited.
        - source .bashrc
      "Which python" now showed  /usr/local/bin/python

      I installed Mongodb using Homebrew, restarted my agent, and saw in the Mongo Dashboard I have available 1 available hosts(now in green!), and in the checks summary I have 0 critical errors.

      This is the article that I used to help solve this issue https://hackercodex.com/guide/mac-development-configuration/



  Creating a Custom Agent Check
      Following the documentation listed here: https://docs.datadoghq.com/developers/agent_checks/

      I made my first custom check following Datadog's simple check instructions for "your first check": https://docs.datadoghq.com/developers/agent_checks/#your-first-check

      I created a hello.py file in the Checks.d folder, and a corresponding hello.yaml file in the conf.d folder, and tested it in the command line using - "datadog-agent check hello".

      For my_metric, I created a my_metric.py file in the Checks.d folder, and a corresponding my_metric.yaml file in the conf.d folder.

      in checks.d/my_metric.py I added the python code:
        from checks import AgentCheck

        from random import randint

        class MyMetricCheck(AgentCheck):
        def check(self, instance):
          randomNumber = randint(0, 1000)
          self.gauge('my_metric', randomNumber)

      In my_metric.yaml I added:

        init_config:

        instances:
          [{}]
        tags:
          - my_metric:tag

      I tested my_metric.py in the command line using "datadog-agent check my_metric"
      I found my check summary in the Datadog dashboard and saw that my_metric has a status of "ok"

  Changing The Check Collection Interval

      In conf.d/my_metric.yaml I changed the instances to include:

        init_config:

        instances:
          - min_collection_interval: 45
        tags:
          - my_metric:tag

      When I restarted the agent for the my_metric check I got the message:
      2018-06-08 14:02:54 EDT | INFO | (scheduler.go:72 in Enter) | Scheduling check my_metric with an interval of 45s

  Bonus Question: I changed the collection interval using the my_metric.yaml file in the above step. I was not able to find documentation on changing the check collection interval using the my_metric.py file.


  Visualizing Data:

    Utilize the Datadog API to create a Timeboard.
    For creating a timeboard, I am using ruby, because I am most experienced in that language.
    I found the documentation here: https://docs.datadoghq.com/api/?lang=ruby#timeboards

    I found the documentation for the rollup method here:
    https://docs.datadoghq.com/graphing/miscellaneous/functions/#rollup-1

    I found the documentation for the anomalies method here:
    https://docs.datadoghq.com/monitors/monitor_types/anomaly/#example

    From the dashboard list, I found my timeboard "Timeboard with my_metric, my_metric rollup, and anomolies on DB FINAL"

    Using my cursor I selected 5 minutes from the graph, which zoomed in the graph to 5 minutes, I then pressed the >> button to show the last five minutes available. The graph showing use of the rollup method  does not show data because it is from the last 5 minutes and not the last 1 hour.

    I took a snapshot using the camera icon, and sent it to myself using @hello@sarahschaab.com.
    I found the snapshot under the "events" tab.

    Bonus Question: What is the Anomaly graph displaying?
      The Anomaly Graph is using anomaly detection. It is an algorithmic feature to help show when a metric is behaving abnormally. 
      https://docs.datadoghq.com/monitors/monitor_types/anomaly/

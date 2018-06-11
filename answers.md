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

  Monitoring Data:

    Warning threshold of 500 created
    Alerting threshold of 800 created
    And also ensure that it will notify you if there is No Data for this query over the past 10m.

    attached screenshots of email alerts "Alert Email.png"

    Bonus Question:
      Please see "Weekday_Downtime_Email.png"
      Please see "Weekend_Downtime_Email.png"

      I could not figure out how to get these times to display in the email as Eastern Time, they appear in UTC.

  Collecting APM Data:
      I configured my datadog.yaml file under apm_config:
        apm_config:

        enabled: true

      According to the Datadog docs, the trace agent needs to be installed separately on macOS https://docs.datadoghq.com/tracing/setup/#setup-process

      install Datadog Trace Agent:
      https://github.com/DataDog/datadog-trace-agent/#run-on-osx

      In order to use the DataDog Trace agent install Go.
      install Go:
      I used the official documentation,
      https://golang.org/doc/install?download=go1.10.3.darwin-amd64.pkg
      Because I have no experience with Go I found this source, more beginner friendly
      http://sourabhbajaj.com/mac-setup/Go/README.html


      Datadog issues: @catalinciurea commented on Apr 23
      https://github.com/DataDog/datadog-trace-agent/issues/397

      I followed these steps and successfully installed Go, I could not get the trace agent running in the foreground to send traces to my dashboard.

      I also attempted following this documentation:
      https://app.datadoghq.com/apm/install
      As well as this documentation:
      http://pypi.datadoghq.com/trace/docs/#module-ddtrace.contrib.flask

      The first time, running
        "ddtrace-run python my_app.py"
      and the second time with the middleware manually installed with
        "FLASK_APP=my_app.py flask run"
      My Flask app was running on localhost:5050, but was failing to send traces.

      I uncommented the "receiver_port: 8126" line in the datadog.yaml file, as one last attempt, but still failed to connect the APM traces.

      I'm disappointed that I was unable to get this section set up, however I am excited because this documentation led me to creating my first "hello world" Go app up and running. I would like to learn more about Application Performance Management, so that I can incorporate it in future apps that I create.

      Bonus Question: What is the difference between a Service and a Resource
      

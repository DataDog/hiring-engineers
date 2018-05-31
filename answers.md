Prerequisites - Setup the environment
      I set up the originally set up a vagrant environment blindly using the defaults given in the link. These defaults provide Ubuntu 12.04. I didn't really run into any issues until I tried to configure the Collecting APM Data Section. This is when I started running into problems. I tried creating another image of 12.04 thinking that I poked around too much on the first image and may have caused a configuration issue. But I ran into the same issue of not being able to download the prerequisites to configure the software.

      I then scraped vagrant all together and used my Ubuntu 16.04 image that already had MySQL installed and installed the Datadog agent on that. Installation of the agent was super easy. I was able to download the prerequisites for Collecting APM Data Section. However, I was not able to get the given Flask application to execute properly. I was however able to run some test trigger successfully.

      One lesson I learned was read the Datadog documentation VERY CAREFULLY. The instructions explicitly state "We strongly recommend using minimum v. 16.04 to avoid dependency issues." Huge mistake on my part... However, by beating my head against the wall, I think I have a better understanding of Datadog because I was forced to look for things that I may have not looked into otherwise.

      Having said this, the Datadog documentation is technically accurate in all the cases that I have referenced. However, there are instances where simply reformatting or adding a few additional cautionary comments would greatly increase the likelihood of success on the first try of an example. For instance, In "Writing an Agent check" https://docs.datadoghq.com/developers/agent_checks/ at about the middle of the page in the section "Your first check", the example explicitly states the file and location, however a simple formatting change, like I reference below, I think, will increase the likeliness of success on the first try.

      Your first check

            The names of the configuration and check files must match. If your check is called mycheck.py your configuration file must be named mycheck.yaml.
            To start off simple, write a check that does nothing more than sending a value of 1 for the metric hello.world. The configuration file is very simple, including no real information.

            conf.d/hello.yaml:
---------------------
            init_config:

            instances:
                [{}]
---------------------

            The check itself inherits from AgentCheck and send a gauge of 1 for hello.world on each call.

            checks.d/hello.py:
---------------------
            from checks import AgentCheck
            class HelloCheck(AgentCheck):
                def check(self, instance):
                    self.gauge('hello.world', 1)
---------------------
Collecting Metrics:

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
    I added a tag in the /etc/datadog-agent/datadog.yaml file.
                tags: my_datadog_yaml_tag:jon

    In order for these tags to be active, the process_config: element must be enabled by also placing the following statement in the  /etc/datadog-agent/datadog.yaml file.

                process_config:
                 enabled: true

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

    I installed MySql database and the agent onto the image. Configuration of the agent was very simple using the following commands:

                sudo mysql -u root -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'p_KOOye63XjZjSBRMwr2s2c8';"
                sudo mysql  -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;"
                sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';"
                sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"

    Running the following commands validated the the configuration was successful. See Screen Shot. Both commands display "MySQL user - OK"

                mysql -u datadog --password='p_KOOye63XjZjSBRMwr2s2c8' -e "show status" | \
                grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
                echo -e "\033[0;31mCannot connect to MySQL\033[0m"


                mysql -u datadog --password='p_KOOye63XjZjSBRMwr2s2c8' -e "show slave status" && \
                echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
                echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"



Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?

    My intial configuation file for the agent was the following
            conf.d/my_metric.yaml:
---------------------
            init_config:

            instances:
                [{}]
---------------------
    As you can see from the screenshot, this gave an interval of approximately 20 seconds. By simply changing the configuration file to the following, I was able to change the collection interval to 45 seconds. Changing the collection interval is also possible by using the python API, however, I think a best practice would be to change configuration files instead of python code. By taking this approach, I also completed the "Bonus Question"
    <img src="https://github.com/jdellaria/hiring-engineers/blob/master/my_metric.png width="500" height="332" />
---------------------
          init_config:

          instances:
                - server: localhost
                  min_collection_interval: 45
---------------------

            checks.d/my_metric.py:
---------------------
            import random
            from checks import AgentCheck
            class MyMetric(AgentCheck):
                def check(self, instance):
                    self.gauge('my_jon_metric', random.randint(0,1001))


Monitoring Data

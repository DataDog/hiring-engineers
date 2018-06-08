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
      - server: mongodb://datadog:<myPassword>@localhost:27017/admin

      In the Datadog Dashboard I navigated to the integrations tab and downloaded the Mongodb Integration.

      I restarted the agent and saw that there was an error with the mongo check connecting to port 27017.
      I removed the .lock file from MongoDB, and still ran into this error.

      In the Mongo Dashboard I have available 1 available hosts, but in the checks summary I am recieving 7 critical warnings under the mongodb.can_connect check.

      I stopped the agent and ran
      - echo "db.auth('datadog', 'ddsolutions')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" && echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"

      When I recieved the output:
      exception: connect failed
      datadog user - OK

      I tried multiple solutions, but continuously ran into this issue.

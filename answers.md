1 . Configured the Agent to connect to the PostgreSQL server by adding the code below to the conf.yaml.example file.
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: anQaBgT9qBf8BXRyR76n9RvQ
       tags:
            - region: california
            - role: database

2 . Added #region: california and role: database tags to datadog.yaml file.  
3 . Installed the respective Datadog integration for PostgreSQL.   
4 . Created checkvalue.yaml file indie the etc directory in order to create custom agent check.
init_config:

instances:
  [{}]

5 . Created checkvalue.py file inside checks.d directory.
from checks import AgentCheck
class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('hello.world', 1)

       

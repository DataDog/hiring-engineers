Datadog Technical Excercise  - Ram Padmanabhan

Prerequisites - Setting up the environment:

-> I spun up Linux 16.04 VM via Vagrant and Installed Datadog agent to receive reporting metrics. 

-> Vagrant configuration. https://drive.google.com/file/d/1KGFLtVo7Tm8kAQilXD-QBuqtqtVD73v8/view?usp=sharing

-> Datadog agent installation successful. https://drive.google.com/file/d/17ZqnrfUAqaT7UgfOBi_joqaOSxOFzSE7/view?usp=sharing

-> Datadog UI receiving reporting metrics. https://drive.google.com/file/d/1tu4ep6oMRSMGrdpdmdjU159ctHaewhkj/view?usp=sharing

Collecting Metrics:

-> Tags added to agent config file.

tags:
    - environment:dev
    - role:server
    - region:eu
 
-> Tags added in agent config file. https://drive.google.com/file/d/19pIHmNzAeJIEWUxr87LJWfxYaL9alSIb/view?usp=sharing
-> Host map. https://drive.google.com/file/d/1tu17YZKAl-dHz4ORVATj3Ujoh-BwGfmX/view?usp=sharing


-> Configured  MySQL Database and Datadog integration for host VM. 

-> Custom Agent Check that submits a metric named my_metric with a random number between 0 and 1000. 

custom_rpcheck.yaml:

init_config:

instances:
    - min_collection_interval: 45


custom_rpcheck.py:

try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck
import random

__version__ = "1.0.0"
class RPCheck(AgentCheck):
  def check(self, instance):
    val = random.randint(1, 1000)
    self.gauge('my_metric', val)


Custom Agent Check Screenshots:

my_metric: https://drive.google.com/file/d/1V54TqYypD0Q1CLLrXhWqKrpcwZaPgjpT/view?usp=sharing
Custom Agent check on host machine: https://drive.google.com/file/d/1rTluBxk2VSbkhLUxXSWOxkAMk_a9yAOI/view?usp=sharing

Visualizing Data:

Utilised DataDog API to create a Timeboard that contains:

-> Your custom metric scoped over your host.
-> Any metric from the Integration on your Database.

Used the bash script to create the timeboard.

api_key=
app_key=

curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "RP Timeboard",
      "widgets" : [{
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ],
              "title": "RP_Metric"
          }
         },
        {
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "avg:mysql.performance.cpu_time{*}" }
              ],
              "title": "RP_MySQL_Metric"
          }
         } ],
      "layout_type": "ordered",
      "description" : "RP Dashboard",
      "is_read_only": true,
      "notify_list": [""],
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "my-host"
      }]
}' \
"https://api.datadoghq.eu/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"

 Screenshots:
RP Timeboard - https://drive.google.com/file/d/1hjjNvlgNBclf959FoST4vU_Y_UAi_ZP6/view?usp=sharing
Time series graph- https://drive.google.com/file/d/1tapi7rCgsRaYE27MOw-BwntYNVOVbg8y/view?usp=sharing
snapshot of this graph sent to my email - https://drive.google.com/file/d/1-0cVQwfx0xVUJh3IH2sVX1cJnZtwx5pZ/view?usp=sharing 

-> What is the Anomaly graph displaying?
The anomaly graph displays or identifies if the metric is behaving differently from the past. Specially the Anomaly graph can be used to forecast to see the high low times.

Monitoring Data:

Created a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

-> Warning threshold of 500 
-> Alerting threshold of 800
-> And also ensure that it will notify you if there is No Data for this query.

Screenshot: https://drive.google.com/file/d/1iOn2JLDrV6C8uAIzgTBXlEEa_X8qtS2n/view?usp=sharing

-> Created different messages based on whether the monitor is in an Alert, Warning, or No Data state.

{{#is_alert}}This is an alert.{{value}}, {{host.ip}}{{/is_alert}} 
{{#is_warning}} This is a warning.{{value}}, {{host.ip}} {{/is_warning}} 
{{#is_no_data}}No Data. {{value}}, {{host.ip}}{{/is_no_data}} 
@ram28nov@gmail.com

screenshots:
Warning - https://drive.google.com/file/d/1t4cZaBMhfKj4zvmKII25Q8rkhUDfQ_SE/view?usp=sharing
Alert - https://drive.google.com/file/d/1HvtbIsZwjo7Fqcaq3M4WSbRGZZyZvq4r/view?usp=sharing

Is there anything creative you would use Datadog for?
Datadog is an amazing tool and can be used in a variety of ways and improves the visualisation and quality of data retrieved. One possible use could to visualise the targets weekly or monthly in a commerce site. Another interesting use would be to retrieve data about when public transports such as buses or trains are the highest peak in terms of crowd. 



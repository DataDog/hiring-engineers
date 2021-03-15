Your answers to the questions go here.
Then, get the Agent reporting metrics from your local machine and move on to the next section...

Collecting Metrics: \
SCREENSHOT OF HOST WITH TAGS and code that created it also links to code file \
INSTALLED POSTGRES SCREENSHOT OF METRICS \
SCREENSHOT OF CUSTOM METRIC and code that created it also links to code file \
I had trouble locating where you put the collection interval line (which file that is). The docs led me to believe at times it was in the agent config file but it also seemed like there was configuration within the custom check file was where you would. I did see that I can change the interval from the datadog UI. 

Visualizing Data: \
SCREENSHOT OF TIMEBOARD \
SCRENSHOT OF TIMEBOARD API CODE/JSON \

SCREENSHOT OF TIMEFRAME \
SCREENSHOT OF SNAPSHOT W @NOTATION \

Is this question asking contexually within the metric itself or a broader context as to what the anomolies function actually does? \
Contextually - Seeing spikes of cpu usage at certain times etc \
Broader Context - Able to determine when incoming datapoints are within a certain expectation or not. \

Monitoring Data: \
Screenshot of monitor \
Screenshot of message building based on which type of threshold and no data notification \
Screenshot of the Email that notifies me \
Screenshots of downtime created \

Collecting APM Data: \
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution: \

Services are the blocks that come together in an architecture at broader scale whereas resources are more the individual pieces of those larger blocks. \
YUCK WORK ON THAT \

Screenshot of Dashboard with Infrastructure and APM Metric \
Please include your fully instrumented app in your submission, as well. \

Final Question: \
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability! \
Is there anything creative you would use Datadog for? \
quantum circuit fidelity /
traffic light / pedestrian traffic /
any sort of large scale system that has multiple pieces working together would benefit absolutely. I think about monitoring flight data from a jet engines to tell when an airline may need to do service on a plane. or even electrical data coming from power grids to help protect against surges and dips. /



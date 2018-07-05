Your answers to the questions go here.
The excercises were very challanging but a really good learning experience. I did have issues with the last one as I could not get PIP or Flask woring correctly in my Vagrant environment. I believe the issue may have something to do with the Ubuntu version that vagrant uses (12.04) but not 100% sure. 
I'm also new to GitHub and I'm not sure how you want me to respond to the questions, I uploaded all the screen shots and files to my fork so I assume you can see them there. The URL for my dashboard that has the exmaples in it can be found here: https://app.datadoghq.com/dash/840545/my-cool-metrics2?live=true&page=0&is_auto=false&from_ts=1529700828621&to_ts=1529704428621&tile_size=m

While I thought the excercises are a good idea and will show how resourceful a candidate is, I think you could add some stuff that would make it better for SE's. I would ask some questions that also have a sales context. Maybe have them create different dashboards for different audiences (app owner, tech lead, IT executive). I see the power of Datadog in it's flexibility and I can see how it would be appealing to developers but how would you pitch it to IT operators or managers, how would it replace some of the existing products out there? Why is it better?

Here are the answers to the invididual tracks:

Collecting Metrics:

Here is a link to a monitored host with custom tags:
https://github.com/pazzman99/hiring-engineers/blob/master/Tags.JPG

This is the code for the "Random Number" metric:

import random
from checks import AgentCheck

class MyRandNum(AgentCheck):

  def check(self, instance): 	
  
    rand_num = random.randint(1,1000)	
    
    self.gauge('My_Rand_Num', rand_num)
  
 Here is a link to the file
 https://github.com/pazzman99/hiring-engineers/blob/master/my_metric.py
 
 Here is the Yaml file code:
init_config:

instances:  
[{}]

Here is the link the the Yaml file
https://github.com/pazzman99/hiring-engineers/blob/master/my_metric.yaml

Bonus Question: Can you change the collection interval without modifying the Python check file you created?
- You can do this by going to metrics/summary and clicking on the metadata edit and change the interval



Here are some of the answers to the bonus questions:
- This is showing deviations from what the system learns is normal operating behavior
I configured the maintenance window for the times specified. There is a screen shot of this in the files.

For the final question, since you can grab metrics from anywhere, it would be really cool to add business metrcis to the technology ones. For example, maybe see $$ of sales aligned with user hits or traffic volumes over time. Maybe even ITOPs stuff like ticket or incident volumes graphed with system performance over time. There are a lot of possibilities. 

In closing I want to thank you for your consideration and really look forward to speaking with you.

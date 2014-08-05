# Datadog Evangelist Challenge
After speaking with Alexis Lê-Quôc on Thursday July 31, I was given the Datadog Challenge late Thursday night/early Friday morning. The challenge included a series of excercises geared to get the applicant up to speed on Datadog's capabilities and to assess the applicant's abilities to follow instructions and read between the lines. I hope I can convince you that I have succeeded on both counts.

***Note:*** *The answers to the questions are called out in the text below in the form of modified paranthetical citations, denoting level and question. e.g.* **(L1Q3)** *means that this is the answer to question 3 in level 1. *

## Level 1

Level 1 involved getting started with the system. This means signing up for the service and installing the Datadog agent. A Datadog Agent is similar in concept to a agent for an intelligence service: it collects the data it was told to gather, performs minimal analysis on that data, then transmits it back to HQ **(L1Q2)**. I installed the agents on **OSX** and **Ubuntu** and pretty quickly had data being collected about the systems' cpu, network, disk, and more.

In addition to agents, there are also third-party integrations. I was eager to see what I could do so I configured the integrations for **BitBucket** and **nginx** which is running on my Ubuntu server on DigitalOcean.

The next step was to submit an event via the API. While I am getting familiar with a RESTful API, I like to use one of the many REST testing harnesses rather than spending time writing code. One that I used here was [Rested](https://itunes.apple.com/us/app/rested-simple-http-requests/id421879749?mt=12). Using this tool, I could enter the endpoint, specifying the authentication info and submit an event. This has the added benefit of allowing me to easily see the full request and response.

![Rested Interface showing an event submission (L1Q3)](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-04%2008.30.28.png)

The final step in level 1 was to get an event to show in my email inbox. I was confused by this until I reread the question just now. It doesn't say this email should be automatic like an alert, just that it should be sent. In order to get any events to show in someone's email, all you have to do is create a comment on the event specifying that person using the *@handle* notation.

So by adding a comment like this:

![Adding a comment](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-04%2008.49.29.png)

I soon see an email in the inbox for m@envl.pe like this:

![Email Notification (L1Q4)](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-02%2011.09.09.png)

At the bottom of the [Alerting Guide](http://docs.datadoghq.com/guides/alerting/), there is a FAQ which covers this: *Can you alert on an event? Not currently, but we're discussing how we'd like to implement this. As an alternative you can set up an @ notification in the body of the event which would deliver the event via email whenever it occurred.* Trying this as follows I got the email in my inbox soon after with no intervention.

![Alerting on an event](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-04%2008.57.43.png)

![Alerted Event Email](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-04%2008.59.04.png)

##Level 2

With level 1 complete, I can now move on to level 2. The first task was to take an existing web app and instrument it using dogstatd to create metrics. I modified my Wordpress theme to increment a value every time the header was shown, every time the home page was displayed, every time a blog post or property listing was formatted and more ***(L2Q1)***. This was simply a matter of using variations of:
```php
Datadogstatsd::increment('aframe_showing_the_header');
```

In order to create an interesting collection of metrics, the next task was to run a load test. One of the tools I enjoy using for this is webpagetest.org which I used to hit the site 15 times each from 20 locations around the world. But there is nothing in the metrics that differ based on location of the viewer, so I switched over to using **ab**, the Apache HTTP server benchmarking tool. 

After a few test runs to verify I had the syntax right, I used ``ab -n 5000 -c 50 http://aframe.envl.pe/`` to hit the page 5000 times, using 50 concurrent clients **(L2Q2)**. This was quite taxing on my server which is the lowest tier on the DigitalOcean platform *(For a while, a $20 dollar donation to the [Changelog podcast](http://thechangelog.com/podcast/) resulted in a $50 credit to Digital Ocean, allowing me to fall in love with the platform.)*

To make this easier to remember later on, I created an event with the command, then commented on it with the results:

![ab command and results](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-04%2009.35.37.png)

In order to get the formatting right on this, I had to specify it as a code block. It is at times like this that I wish the platform supported MultiMarkdown rather than simply Markdown. Using tables would have been nice here.

![home page ab test (L2Q2)](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-03%2021.33.29.png)

 To see what this did to my server, check out this chart of the cpu at the time:

 ![cpu utilization](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-03%2021.35.53.png)

The final stage for level 2 was to create a histogram to see the latency. Now I have to admit I was confused by this one. The way I define latency in this context is the time between the client requesting the page and receiving the first byte. This implies that the client is performing the timing, but there is no javascript library for dogstatd. Performing the timing on the server is ok, but there is no way to get the full picture since you are already a few milliseconds in when starting the timer. Then, the graph that would apply to this is designed to show a distribution across hosts and not for my use. Finally, the histogram method in dogstatd seems to apply the distribution algorithms close to data collection time rather than at analysis time. As some one who has spent a little time in R analysing regular web traffic data, that seemed odd.

But here is what I ended up with. I record the current time when the theme first begins to load up in the functions.php file. Then at the end of the footer, I figure how much time was spent processing the request. This is then submitted to dogstatd using the call: ``Datadogstatsd::histogram( 'aframe_histo_page', $runtime)``. Then to graph the results, I show a timeseries looking at the max, 95percentile, avg, and median values. This gives me a kind of sideways distribution over time. Here is a snapshot of it:

![Histogram (L2Q3)](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-03%2013.25.02.png)

Here is the final dashboard:

![Dashboard (L2Q4)](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-03%2013.29.01.png)

##Level 3

Level 3 builds on from level 2, using tags to introduce an extra level of meaning to our graphs. The first step was to add the tag 'support' to all metrics. This is simply a matter of adding another parameter to the calls: ``Datadogstatsd::increment('aframe_showing_the_header',1,array('tagname'=>'support'));`` **(L3Q1)**. 

The next step was to tag the metrics per page. So the home would be page:home, etc. At first I thought this meant I had to have tags with the full text 'page:home'. Later I realized that 'tagname' wasn't a required array key. The key in the tags array could be anything, including 'page'. All I had to do was create a function to output the page name, then modify my histogram call at the bottom of the footer to: ``Datadogstatsd::histogram( 'aframe_histo_page', $time, 1, array('tagname'=>'support','page'=>page_tag()) );`` **(L3Q2)**. That page_tag function looks like this (still very rough and could be refactored to half):

```
function page_tag(){
//  $retval = 'page-';
    $retval = '';
    $requri = $_SERVER["REQUEST_URI"];
    
    if ($requri == '/')
        $retval .= 'home';
    elseif (strpos($requri,'listings-search'))
        $retval .= 'listings-search';
    elseif(strpos($requri,'blog'))
        $retval .= 'blog';
    else
        $retval .= basename($requri);
    return $retval;
}
```

You can see some of the 'page' tags in this dropdown for the $page template variable:

![available tags](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-03%2020.51.45.png)

The final step in level 3 is to revisit the latency using these new page tags. You can see my results here:

![avg](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-03%2016.20.32.png)

I wish I could change my tag and scope template values from this zoomed in view.

##Level 4

Level 4 focuses on getting page views graphed. I had already started collecting the data for these at the beginning by calling increment on the page header which is at the top of every page **(L4Q1)**. Since I was now recording page name in the tag, being able to correlate the page views to specific pages was much easier. 

![page counts (L4Q2, L4Q3)](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-03%2021.39.16.png)

When looking at a view of the results from the last day, you can see that the bars are stacked showing counts for each separate page seen in that time slot. 
![last day of page views (L4Q3)](https://dl.dropboxusercontent.com/u/261923/Screenshot%202014-08-04%2010.26.10.png)

While the graph does not appear to be spiky in this format, it would appear so when using lines. This is a result of looking at a single measurement from a short test in a large timeslot. If the time interval were a minute and there were 5 hits per minute for 5 minutes, then 4 hits the next minute, then 3 hits the next minute, then 2, then 1, the chart would look much smoother. Due to the mashing up of a low resolution graph with a high resolution test, the graph appears 'spiky' **(L4Q4)**.

##Level 5
The last level in the challenge (apart from writing it all up) is to modify the agent with a custom check. The documentation guides the user through creating a check but misses a key point not obvious to someone who doesn't spend a lot of time in Python. The code sample used in the guide is as follows:
```
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', 1)
```

But when this is executed, you get a warning that AgentCheck is an unknown name. The solution is of course a missing import, but if you don't use Python every day, you may give up here. Correcting this and adding the random data gets the answer to the last step of the challenge **(L5Q1)**:

```
from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
```

##Conclusion
And that brings me to the end of the challenge. I found it to be an interesting and fun way to get up to speed on the Datadog platform. I like that the platform has a lot of features that the right audience will definitely pay for. I also like that there are enough issues that I encountered in my short time with it which need to be solved before it is perfect. This means that I get an ongoing challenge coming up with short-term workarounds as well as helping devise long-term fixes. I like the nice blend of end-user features with developer extensibility. This means that an evangelist like me could have a fun and exciting future with this company.

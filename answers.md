## Section 1: Collecting Metrics

After looking over the challenges given to me to introduce me to Datadog's product, my first thought was, "Wow. I might be in over my head here". I have had limited experience with monitoring software in my career, and when first looking at everything that Datadog can do, it certainly felt overwhelming. However, no great things come easy so I got to work. After downloading the Agent to my machine, I almost immediately started to see metrics being reported. Aside from downloading the Agent, my first defined task was adding tags to the agent config file and show that they successfully carried over to Host Map page in Datadog. This task seemed pretty straightforward, and after finding the config file and adding the tag, it appeared in the Host Map page.
![Tag in Agent Config](tag_within_agent_config_file.png?raw=true "Tag in Agent Config")
![Tag on Host Map](tag_on_host_map.png?raw=true "Tag On Host Map")
As a side note, you can see that the tag on the host map reads a bit differently than the actual tag in the Agent config file. I assume that this is the way to handle apostrophes in a string.

My second task was to install a Datadog integration on a database on my machine. Luckily, I already had PostgreSQL on my machine and have used it extensively for projects and assignments from my time at Launch Academy. After creating a Datadog User with read-only access via the command line (`create user datadog with password '<PASSWORD>';
grant pg_monitor to datadog;`), I again was given confirmation of this step nearly immediately within the Datadog interface in my list of instances as well as on the integrations page.
![List of Instances](List_of_instances.png?raw=true "List of Instances")
![PostgreSQL Installed](postgres_installed.png?raw=true "PostgreSQL Installed")

Next up I was tasked with creating a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000. This aspect took a little longer for me as I had a small syntax error in generating a random number for each check. But I figured it out! By using this code: `import random
from random import randint


try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge(
            "my_metric",
            random.randint(0, 1000),
            tags=["TAG_KEY:TAG_VALUE"],)`
I was able to create my_metric. This is a very bare bones usage of it, but it does indeed work according to the timeseries graph I created on the Dashboard page.
![my_metric Timeseries](my_metric_timeseries.png?raw=true "my_metric Timeseries")
Next I had to change the interval of my check's collection interval to once every 45 seconds. I did this by going into the accompanying yaml file for my_metric and setting "min_collection_interval" to 45. It is my understanding that the "min_collection_interval" doesn't necessarily guarantee a solid interval every X amount of seconds, but rather the minimum amount of time a collection is made depending on the amount of other integrations enabled on the Agent.

Bonus question time! It appears that another way to change the collection interval without modifying the Python check file is to do it directly within your Dashboard. When you click on the widget settings button, you can edit the interval time.
![Change Interval](change_interval.png?raw=true "Change Interval")

## Section 2: Visualizing Data

This section definitely proved to be a bit more difficult for me. After reviewing the docs and trying a few things out I was finally able to create a dashboard via the Datadog API. However, I was not able to create two widgets simultaneously with one API call. I know that there is something wrong with the layout of my file, but I just can't seem to get it quite right (I'm hoping to get some clarity on this down the road). This is the script that I used:
`from datadog import initialize, api

options = {
    'api_key': '648c3e89d8d364910175fc7ab0ac93b5',
    'app_key': '65997f7ab341dde29853243be978212c06c1af8b'
}

initialize(**options)

title = 'API Test Dashboard 2'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}.rollup(sum, 3600)'}
        ],
        'title': 'My Custom Metric'
    }
}]


layout_type = 'ordered'
description = 'A dashboard to test the API.'
is_read_only = True
notify_list = ['user@domain.com']
template_variables = [{
    'name': 'MacBook-Air',
    'prefix': 'host',
    'default': 'MacBook-Air'
}]

saved_view = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': 'MacBook-Air'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_view)
`
You will notice in the above script that I implemented the rollup feature. This function takes two arguments, the method (sum, min, max, count, avg), and the time (in seconds). So per the challenge, I setup my_metric to have the rollup feature with a sum method set to 1 hour (3600 seconds) interval between the data points.
It also appears in the documentation that setting custom time frames is still in beta. Maybe this is why I couldn't properly get the last 5 minutes to show.
![Custom Timeframes](custom_timeframes.png?raw=true "Custom Timeframes")
I was able to send a snapshot of myself though, with the graph set at "The Past 15 minutes".
![Snapshot](snapshot.png?raw=true "Snapshot")

## Section 3: Monitoring Data

Let me just say that I thoroughly enjoyed this section of the challenge, as I really like working with the Datadog interface. I found that setting up the Metric Monitor was really straight forward. Here is how I set it up:
![Metric Monitor setup](alert_setup.png?raw=true "Metric Monitor setup")
![Metric Monitor text](alert_text.png?raw=true "Metric Monitor text")
Resulting email (this screenshot is from a test however):
![Email Monitor](email_monitor.png?raw=true "Email Monitor")
I did have difficulty on getting the value that triggered the monitor to show up properly in the email alerts, and would love more insight on this. (You can see this indicated in the email by "0.0 caused this Alert")

This obviously resulted in my email inbox being bombarded so the second part of this challenge was a welcome one. I was tasked with creating downtimes for this monitor that silences it daily M-F from 7pm-9am, as well as all day on Saturday and Sunday. I also had to make sure an email was sent once I confirmed these down times.
![Silence Alert](silence_alert.png?raw=true "Silence Alert")
Resulting email notification:
![Email Silence](email_of_silence.png?raw=true "Email Silence")
(At first I thought I botched the times, admittedly. But after checking the UTC times, it was indeed correct)

## Section 4: Collecting APM Data:

This section took me the most time, hands down. It wasn't necessarily my understanding of the content, but rather a ton of issues with my machine and how I had everything setup. Initially I tried to solve this challenge with an older project that I built on Rails, but a fairly prevalent OpenSSL issue shut that down pretty quick. My next plan of action was to completely upgrade Ruby on my machine and see if that remedied the issue...it didn't. My next plan of attack was creating a brand new, very simple Sinatra app but I couldn't get it quite right. So it was then time for plan C. I have never built or used a Flask app in my life, but there is no better time to learn! After following the documentation I was pretty sure I was ready to fire it up and get to work. I was slightly off on that assumption. I found that the defined port number in the script that was provided to me (5050) was already in use by my Dropbox application. After changing the port number to 8910 in the script, and running "ddtrace-run python hello.py", I was up and running! It certainly is not a complex application by any standards, but at this point in time I preferred to keep it as simple as possible to understand what was happening in the script in terms of api entry points, apm endpoints, and trace endpoints. The dashboard can be found [here](https://app.datadoghq.com/apm/trace/8257436633630229529?spanID=5860849188908287769&env=none&sort=time&colorBy=service&graphType=flamegraph&shouldShowLegend=false)

![APM Dashboard](APM_screenshot.png?raw=true "APM Screenshot")

**Bonus**
It is my understanding from the documentation that Resources are what makes up Services. An example of this would be a website that has a merchandise section of their website. They may have group of endpoints such as their "add item", "payment", and "checkout" as their "store" Service. The individual endpoints within those mentioned above would make up the Resources for that Service.

## Final question
While researching Datadog in the weeks leading up to me applying, and during this exercise, I have had a lot of "a ha!" moments in terms of what is possible with this software. When I saw this question I honestly got pretty excited to share an idea with you all on how I think this software can be leveraged in today's world. As we all know, the standard workday isn't quite the same as it was a few months ago, before the COVID-19 pandemic. Pretty much every tech company in the United States (and some non-tech) went virtual/work from home to keep their employees safe. Now, as it stands today, more and more states are re-opening and allowing employees to go back to the office to work. However, there have also been some very large companies who are now considering staying remote for either the rest of the year, or for the foreseeable future. I think Datadog could be used in extremely beneficial ways to companies who are weighing their options of either going back to physical offices, or staying virtual/remote forever. They would be able to see how employees perform in both scenarios; how many bugs are created whether employees are at home or in the office. The ability to track tickets from clients and how fast fixes are pushed out to remedy them. Not to mention the ability to see how clients interact with your site while they are likely stuck at home. How would those interactions translate to a more "normal" world when restrictions are lifted and people leave their houses (and computers) more often?

## Wrap-up
I would just like to say how great this challenge was overall. It has been quite some time since I've been challenged to understand a technology all on my own, but it really is the best way to learn it. I truly appreciate all of your time and I look forward to hearing from you soon. If there are any glaring changes that need to be made to this, please let me know and I would be happy to make them!

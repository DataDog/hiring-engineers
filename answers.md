Level 1/

Thank you for choosing Datadog!

To start your journey with us, please sign up for free here https://www.datadoghq.com/pricing/ .

At the end of the sign up process, you'll be given your API key, a 32 characters long hexadecimal string. Please record it, we'll need it later.

Then, you'll need to install the agent. The agent is a piece of software running on your machine that is here to collect events and metrics from 
your machine or other elements in your infrastructure. For more information about the agent, please visit http://docs.datadoghq.com/guides/basic_agent_usage/ .

You can download the agent for your operating system here https://app.datadoghq.com/account/settings#agent

On a Linux machine you can simply run the following command :

```
#DD_API_KEY=your_api_key_goes_here bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```

To check that is is started run the following command : 

```
#/etc/init.d/datadog-agent status
Datadog Agent (supervisor) is running all child processes
```

If you're running a modern version of Windows you can use this oneliner from an elevated powershell session :

```
Invoke-WebRequest -Uri https://s3.amazonaws.com/ddagent-windows-stable/ddagent-cli.msi -OutFile ddagent-cli.msi | msiexec.exe /qn /i ddagent-cli.msi APIKEY="your_api_key_goes_here"
```

To check that it is started run the following command :

```
get-service -Name DatadogAgent

Status   Name               DisplayName
------   ----               -----------
Running  DatadogAgent       Datadog Agent
```

Now let's take a look at the Event Stream. 

The Event Stream allows you to browse what happened in your infrastructure and looks like a timeline. It also works similar to a blog : you can post events to it, comment events or search for events using different criteria.
To look at your event stream, visit this page https://app.datadoghq.com/event/stream

We'll try to create an event programmatically using Datadog's REST API. You can find the API documentation here http://docs.datadoghq.com/api/ . Today, we'll be using the 'events' endpoint. And because we want to post an event, we'll use the 'POST' HTTP method.

If you are running Windows, take a look at the Powershell code in New-DataDogEvent.ps1, then in a Powershell session run :

```
. .\New-DatadogEvent.ps1
New-DataDogEvent -title "Apache seems down" -text "Looks like it's using all the memory!" -ApiKey "your_api_key_goes_here"
```


You should get a response with Status Code OK and you should see the event on your Stream.

If you are on Linux, pasting this into your prompt should give you the same result : 

```
curl  -X POST -H "Content-type: application/json" \
-d '{
      "title": "Apache seems down",
      "text": "Looks like it's using all the memory!",
  }' \
'https://app.datadoghq.com/api/v1/events?api_key=your_api_key_goes_here'
```

Did you know that Datadog has a notification system built into the Event Stream? 

Try to enter the  following in the 'text' statement of your request :
"@your@email.domain message" where "your@email.domain" is the email you have signed in with and "message" is the content of your message.

You can look at the file screenshot-level1-api-email.PNG to see what the email looks like. 

You can find out more about the @ notifications here http://docs.datadoghq.com/faq/
 


Level 2/

Welcome back!

Today we'll see how we can send custom data to Datadog's Agent.

For that we'll use a subsystem of the agent called Dogstatsd. It is a StatsD server customized by Datadog. We can use any StatsD client to send data to Dogstatd, but Datadog's client give you some extra features.

You can  get more information about it here http://docs.datadoghq.com/guides/metrics/ .

Datadog and the Community have created several libraries that will allow you to talk to Dogstatsd using your favorite language. The libraries are listed here http://docs.datadoghq.com/libraries/ .


Today we'll create a very simple PHP Web App and see how we can use the php-datadogstatsd librarie. Documentation can be found here https://github.com/DataDog/php-datadogstatsd/blob/master/README.md .

We'll create a PHP page that displays the date and collects some metrics using Dogstatsd :

```
<?php

require './libraries/datadogstatsd.php';

echo date('l jS \of F Y h:i:s A');

//we implement the value of the web.page_views by 1 (default for increment)
//metrics must use a hierarchic naming
DataDogStatsD::increment('web.page_views'); 

?>
```

To generate some load on our App, we use the Apache Benchmark tool :

```
simon@ubuntu-01:~$ ab -n  200 -c 3 http://URL-OF-YOUR-APP
[...]
Concurrency Level:      3
Time taken for tests:   0.218 seconds
Complete requests:      200
Failed requests:        0
Total transferred:      45600 bytes
HTML transferred:       8200 bytes
Requests per second:    917.78 [#/sec] (mean)
Time per request:       3.269 [ms] (mean)
Time per request:       1.090 [ms] (mean, across all concurrent requests)
Transfer rate:          204.35 [Kbytes/sec] received
[...]
```

Now let's visualize this information using Datadog's graphs.

Go to the Infrastructure tab and click on your host. Then click on the 'Clone this dashboard' icon in the top right corner, give it a name and clone it.

Then click on 'Edit dashboard' and add a 'Time Series' widget. Choose the metric 'web.page_views', select 'Compute as rate/sec', 'Take the average' and 'Display it as Seperate lines'. Give it a name and save it.

You can find an example here https://app.datadoghq.com/account/settings#2b11d05fb90ab314e6dfa55686fc7a1cec4660f24aa7d4dc4270480ec7c20ff3 or look at the file screenshot-level2-ab-benchmark-web.page_views.PNG .


Now let's introduce some latency in our application, and monitor it :

```
<?php

//let's start timing the execution from
$start_time = microtime(true);

require './libraries/datadogstatsd.php';

$sleepy_time=rand(1, 100) / 100;
sleep($sleepy_time);

echo date('l jS \of F Y h:i:s A');

//we implement the value of the web.page_views by 1 (default for increment)
DataDogStatsD::increment('web.page_views');  
//we create an histogram for the execution time
DataDogStatsD::histogram('web.execution_time', microtime(true) - $start_time);

?>
```

Here we are using an histogram, to measure the statistical distribution of values.

Creating one histogram will create the following metrics : 

```
web.execution_time.count
web.execution_time.avg
web.execution_time.median
web.execution_time.max
web.execution_time.95thpercentile
```

Showing the 95th percentile in a graph next to the Median and the Average might give you a good idea of how your top queries are performing compared to the othe ones.

You can find such a graph here https://app.datadoghq.com/graph/embed?token=a5db3ea9fe1100a7f6e7c125252df08d09fbdb73640d3135857e0d63e0218e16&height=300&width=600&legend=false or take a look at the file screenshot-level2-execution-times.PNG .


Level 3/


Now let's look at a neat feature of Dogstatsd, the tags.

Tags allow you to add some insight to the metrics your produce with your code, with information that makes sense to you. Tags are a feature of Dogstatsd, so you'll need a compatible client.

Let's add two pages to our Web App so we end up with the following pages :

```
index.php
fastpage.php
slowpage.php
```

Now we can tag these pages as being part of the `support` tag, this way :

```
DataDogStatsD::increment('web.page_views', 1, array('support'));
```

As you can see, the third argument is an array, so we can put as many tags as we want, though Datadog recommends to keep it under 1000 tags per metric.


Let's add a second tag to our metrics that will allow us to differentiate our pages : 

```
//for index.php
DataDogStatsD::increment('web.page_views', 1, array('support','pagename' => 'page:index'));
DataDogStatsD::histogram('web.execution_time', microtime(true) - $start_time, 1, array('support','pagename' => 'page:index'));
```

The tag can take a key:value syntax, this will allow us to break down or metrics per 'key' in our graphs. For example, it's easy to stack the latency per `pagename`, see screenshot-level3-stacked-latency-per-page.PNG.


Level 4/

Welcome back! Let's keep on working with Dogstatsd and graphs for a moment.

If all the pages in our Web App increment the `web.page_views` metric like in previous exercise, then we can count the number of pages that were visited and we can slip it by page. 
Actually, we can do that on a single graph, see the file screenshot-level4-page-views-and-page-views-by-page.PNG. You'll notice that the line of `sum:web.page_views{*}.as_count()` and the top line of `sum:web.page_views{*} by {pagename}.as_count()` have the same value, that's normal.




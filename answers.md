# Answers

## Level 1
**What is the agent**:

* It is a software that runs on the host, which in this case is an Amazon Linux. An agent uses its built in code to send host metrics as well as user generated metrics. The general purpose of adding a agent to a host is to automatically monitor the host performance with its bulit in dashboards and agent sub tools:
    * __Collector__: It incldues pre scripted checks for the host and depends on the type of the host it is installed on as well as the additional Datadog integrations installed on the host. Sample of common collected metrics will be CPU, memory, storage and IO performance.
    * __DogstatsD__: The running user-created application on the host will send its custom metrics   to this backend statsD server.
    * __Forwarder__: The metrics from both the collector and DogstatsD will be quesued and sent via the forwarder to Datadog's servers.
* Agent Dashboard
  * [link for the agent's dashboard](https://p.datadoghq.com/sb/34cc3a8175)
  * Used a screenboard, which can be shared and this specific one contains the following graphs:
    * Load AVGs (avg of ``` system.load.1+5+15``` metric)
    * Disk IO wait (max of  ```system.io.await``` metric)
    * CPU % (using JSON):

```

{
  "viz": "timeseries",
  "requests": [
    {
      "q": "system.cpu.idle{host:i-6e573182}, system.cpu.system{host:i-6e573182}, system.cpu.iowait{host:i-6e573182}, system.cpu.user{host:i-6e573182}, system.cpu.stolen{host:i-6e573182}"
    }
  ]
}

```


** Submit an event with the API **:

* Using the DogstatsD python client imported as ```statsd```, we can create an event with ```statsd.event('<event title>','<event description>')```
* [Event link](https://app.datadoghq.com/event/event?id=2599350133770195633)

## Level 2
**web app**:

It is a python app using flask (app.py) that contains three basic functions: the default index page output, "Hello world" output and current date output.

The load test uses ab (Apache Benche):

* __Syntax __: ``` ab [options] [http[s]://]hostname[:port]/path``` Options and host used:
  * ``` -k ```: Enable keep alive feature, which allows multiple requests within one HTTP session. Default is disable keep alive feature
  * ```-n <NUM>```: Number of requests to be during the benchmarking session. Default is just one request.
  * ```-c <num> ```: Number of multiple requests to issue at a time, depends on the keep alive feature. Default is one requests at a time.
  *```-t <num> ```: Maximum number of seconds to spends on the benchmarking. Default is no limit.
  * Since we are running test locally on the host, the host name will be ```127.0.0.1``` and the port is ```5000```. The different path include:
    * ```/``` for the index
    * ```/hello``` for hello world
    * ```/time``` for the current time


* __Actual index page command__:
```
ab -k -n 500 -c 100 -t 20 http://127.0.0.1:5000/
```
* __Index page Output__:

```
This is ApacheBench, Version 2.3 <$Revision: 655654 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/
Benchmarking 127.0.0.1 (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Finished 22015 requests

Server Software:        Werkzeug/0.9.6
Server Hostname:        127.0.0.1
Server Port:            5000

Document Path:          /
Document Length:        51 bytes

Concurrency Level:      100
Time taken for tests:   20.000 seconds
Complete requests:      22015
Failed requests:        0
Write errors:           0
Keep-Alive requests:    0
Total transferred:      4491060 bytes
HTML transferred:       1122765 bytes
Requests per second:    1100.73 [#/sec] (mean)
Time per request:       90.848 [ms] (mean)
Time per request:       0.908 [ms] (mean, across all concurrent requests)
Transfer rate:          219.29 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.3      0       5
Processing:     2   91   4.2     90     111
Waiting:        1   90   4.2     90     110
Total:          5   91   4.0     90     111

Percentage of the requests served within a certain time (ms)
  50%     90
  66%     91
  75%     91
  80%     92
  90%     92
  95%     93
  98%     97
  99%     99
 100%    111 (longest request)
```
* __Output analysis__ (except the confirmation of the used options, host and port ):
  * Completed requests - 22015
  * No failed requests or write and errors
  * Total bytes and HTML bytes transferred
  * Additional rates (Mean):
    * requests per second rate
    * time per request in ms
    * time per request in ms for all concurrent requests

 * [Histogram of Latency](https://p.datadoghq.com/sb/145eb484e6): sum of ```page.view.time.avg ```

* [Additional Dashboard](https://p.datadoghq.com/sb/1b397b86b8):
  * sum of ```page.views``` computed ```as count```
  * avg of ```datadog.dogstatd.packet.count```
  * avg of ```system.cpu.user```
  * Event time liner of everting for the past week


## Level 3
* [Dashboard link](https://p.datadoghq.com/sb/b0c792db21)
  * avg of ```page.view.time.avg``` by ```page```
  * avg of ```page.view.time.avg``` by ```*```
  * avg of ```page.view.time.avg``` by ```page:page0```
  * avg of ```page.view.time.avg``` by ```page:page1```
  * avg of ```page.view.time.avg``` by ```page:page2```


## Level 4
* [Dashboard Link](https://p.datadoghq.com/sb/f2056727fb)
  * sum of ```page.view.time.count``` by ```page``` computed ```as count```
  * sum of ```page.view.time.count``` computed ```as count```
  * sum of ```page.view.time.count``` by ```page:page0``` computed ```as count```
  * sum of ```page.view.time.count``` by ```page:page1``` computed ```as count```
  * sum of ```page.view.time.count``` by ```page:page2``` computed ```as count```



__ The graph are very spiky for two possible reasons__:

* First, it depends on the time range, meaning that once a time range is small enough the graph would level out.
* Second, the load tests create a huge amount of load on the web app, which in turn creates a sharp spike figure on the graph

## Level 5 ###
* Can be found in se.yaml and se.py
  * ```se.yaml```:

  ```
  init_config:
    default_timeout: 10
instances:
    - url : http://127.0.0.1:5000/

    - url : http://127.0.0.1:5000/hello

    - url : http://127.0.0.1:5000/time
    ```
    ```init_config``` allows for global configuration options


    ``` default_timeout: 10 ``` is the defined timeout to use in case of no response
  * ```se.py```:

  ```
  from checks import AgentCheck
import random
class support(AgentCheck):
    def check(self, instance):
        x = random.random()
        self.gauge('test.support.random', x)
    ```
    ```instances``` section includes which hostname and port would the check run on.
* [Dashboard](https://p.datadoghq.com/sb/4ea76a0d3b): avg of ```test.support.random```

## Level 6
### Prep-work
* I started with setting up a DataDog trial account with the email iftash@gmail.com
* AWS EC2 instance with a secured VPC and a Amazon Linux AMI
* I installed the Amazon linux agent and started following the questions/levels.
  * Level 1: I created the initial event, when I enabled the agent on the AWS instance.
   I created a basic python app that uses Flask and DogstatD and created some events with it.
   * Level 2: I used ab to run the load tests and created screenboards, so I could share the outputs. Same goes for the histogram and additional screenboards
   * Level 3: I created multiple pages and tagged them both with the support tag as well as the page number tag with graphed their latency on a screenboard. I ran the load test for each of the tags as well.
   * Level 4:  Using the previous tags I created a screenboard with that graph the page view count per page.
   *Level 5: I created a basic agent check, that goes outputs a random number for a test.support.random metric and created a screenboard for it

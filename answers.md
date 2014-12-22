# Answers

## Level 1
* Name of agent: Amazon Linux
* Agent is installed on a AWS host

[link for the agent's dashboard](https://p.datadoghq.com/sb/34cc3a8175)

[Event link](https://app.datadoghq.com/event/event?id=2599350133770195633)


## Level 2
web app: a python app using flask => app.py

Load test via ab:

* Load Test Command
```
ab -k -n 500 -c 100 -t 20 http://127.0.0.1:5000/
```
* Output:

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

 * [Histogram of Latency](https://p.datadoghq.com/sb/145eb484e6)


* [Additional Dashboard](https://p.datadoghq.com/sb/1b397b86b8)

## Level 3
[Dashboard link](https://p.datadoghq.com/sb/b0c792db21)

## Level 4
[Dashboard Link](https://p.datadoghq.com/sb/f2056727fb)

### The graph are very spiky for two possible reasons:
* First, it depends on the time range, meaning that once a time range is small enough the graph would level out.
* Second, the load tests create a huge amount of load on the web app, which in turn creates a sharp spike figure on the graph

## Level 5 ###
* Can be found in se.yaml and se.py
* [Dashboard](https://p.datadoghq.com/sb/4ea76a0d3b)

## Level 6
### Prep-work
* I started with setting up a DataDog trial account with the email iftash@gmail.com
* AWS EC2 instance with a secured VPC and a Amazon Linux AMI
* I installed the Amazon linux agent and started following the questions/levels.
  * Level 1: I created the initial event, when I enabled the agent on the AWS instance.
   I created a basic python app that uses Flask and DogstatD and created some events with it.
   * Level 2: I used ab to run the load tests and created screenboards, so I could share the outputs. Same goes for the histogram and additional screenboards
   * Level 3: I created mutliple pages and taged them both with the support tag as well as the page number tag with graphed their latency on a screenboard. I ran the load test for each of the tags as well.
   * Level 4:  Using the previous tags I created a screenboard with that graph the page view count per page.
   *Level 5: I created a basic agent check, that goes outputs a random number for a test.support.random metric and created a screenboard for it

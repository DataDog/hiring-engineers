<h1>Support-Engineer Technical Exercise<small> - Tyler Pendleton</small></h1>

##1##
What is the Agent?
----------------
<h3>The Agent is the software that runs on my hosts.  It collects events and metrics and reports them to Datadog.</h3>
<h2>Submitting an Event</h2>
<h3>Here is the code that I used to submit my first event</h3>
```ruby
1 require 'rubygems'
2 require 'dogapi'
3 
4 api_key = '3d0d5a2fc177675caa4b879daa2780fb'
  5 
6 dog = Dogapi::Client.new(api_key)
  7 
  8 dog.emit_event(Dogapi::Event.new('Creating my first event', msg_title: 'My First Event'))
  ```
  <h4>Getting the event to appear in my email inbox</h4>
  <p>I replaced the line 8 message of 'Creating my first event' with '@tyler@tylerpendleton.com'</p>

  ```ruby
  8 dog.emit_event(Dogapi::Event.new('@tyler@tylerpendleton.com', msg_title: 'My Second Event'))
  ```
  ![enter image description here](https://lh3.googleusercontent.com/-2Oa2eX8CUFI/VnCtvD5WG_I/AAAAAAAABYs/pF2HfhSdK5o/s0/Screen+Shot+2015-12-15+at+4.39.48+PM.png "Screen Shot 2015-12-15 at 4.39.48 PM.png")

##2##
  [Link to Question 2 Graphs](https://p.datadoghq.com/sb/188ad36eb-a27bd341aa)
  ![enter image description here](https://lh3.googleusercontent.com/-WB7qGkpDft8/VnHXAwsr53I/AAAAAAAABa4/sC4S99odoqg/s0/Screen+Shot+2015-12-16+at+4.25.49+PM.png "Screen Shot 2015-12-16 at 4.25.49 PM.png")

##3##
  [Link to Question 3 Graphs](https://p.datadoghq.com/sb/188ad36eb-04bfe4c544)
  ![enter image description here](https://lh3.googleusercontent.com/i4o11cxvXbT6tNciz40wdub7T5Pyhb4GWhGqVoav14Wgf1YGF7XFsRpYzE9ZtR7RQLXh=s0 "Screen Shot 2015-12-16 at 1.49.03 PM.png")

##4##
  [Link to Question 4 Graphs](https://p.datadoghq.com/sb/188ad36eb-40f1b6403f)
  ![enter image description here](https://lh3.googleusercontent.com/-EpsEGk8MzHI/VnGykm14U1I/AAAAAAAABZs/dr8BIGgy-DQ/s0/Screen+Shot+2015-12-16+at+1.48.14+PM.png "Screen Shot 2015-12-16 at 1.48.14 PM.png")
  <h2>Why are the graphs spiky?</h2>
  <h4>The graphs are spiky because they are receiving different data at every point. Over time(x) the page views/load times/data points(y) will vary per second, increasing or decreasing, creating spikes and valleys in the graph.</h4>


##5##
  ```python
#random_check.py

import random
from checks import AgentCheck
class RandCheck(AgentCheck):
    def check(self, instance):
	self.gauge('test.support.random', random.random())
```

```yaml
#random_check.yaml

    init_config:

    instances:
        [{}]
```
[Link to test.support.random graph](https://p.datadoghq.com/sb/188ad36eb-d0cf596a6f)
![enter image description here](https://lh3.googleusercontent.com/-8WTFfcjMX7U/VnHUQRb9pxI/AAAAAAAABao/AprNCQr6bLQ/s0/Screen+Shot+2015-12-16+at+4.14.29+PM.png "Screen Shot 2015-12-16 at 4.14.29 PM.png")

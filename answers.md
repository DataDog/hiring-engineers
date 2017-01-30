
## Answers

### Level 1

What is the agent?:
    The agent is software that runs on a user's hosts (for example, 
a server hosted by Amazon EC2) and gathers system metrics data 
(for example, CPU usage) as well as custom metrics data from the 
user's applications (for example, data on traffic to a webpage). 

To submit an event via the API, I ran the 
following code in the Python shell from terminal:

```
>>> from dogapi import dog_http_api as api
>>> api.api_key = '7ecedff550b31c42b5237566f2dc1a2c'
>>> title = "Testing event!"
>>> text = 'This is a test event to my inbox! @lwthree@princeton.edu'
>>> tags = ['test']
>>> api.event_with_response(title, text, tags=tags)
2660614202829760793
>>> 
```

In the text variable, I use the @username notation to send an email 
notification to my username (currently lwthree@princeton.edu).
The api key on the second line was obtained from 
https://app.datadoghq.com/account/settings#api

An event has now appeared on my Datadog feed.

<img src="https://dl.dropboxusercontent.com/u/806656/datadog1.png">

The event has also been sent as an email to my inbox.

<img src="https://dl.dropboxusercontent.com/u/806656/datadog2.png">


### Level 2

The web app I am experimenting with for this challenge is Frogg--a simple 
blog that has two main pages: an index page that displays all posts,
and an add_entry page for adding new posts. 

To run the load test, I used Siege (http://www.joedog.org/siege-home/).
For the load test, I randomly sieged/visited the index page and the 
add_entry page. The metric I created for these experiments is called
web.page_hit which is incremented everytime there is a page hit to either the
index page or the add_entry page.

<img src="https://dl.dropboxusercontent.com/u/806656/loadtest1.png">

In the above image, three load tests were run on the Frogg web app, with 
the first starting around 23:13, the second starting at around 23:18, and the 
third starting around 23:31. Each load test was simulated as three concurrent 
users randomly visiting the index and add_entry pages with a random delay of up to 10s
between visits. The line in the above graph represents the average hits/sec for 
all pages of Frogg. Shown below is the live graph. 

<iframe src="https://app.datadoghq.com/graph/embed?token=230ce0b8d5714b46cc7d7fafc4e6d8543b6d165f7d0950b5efc261c57d864b76&height=300&width=600&legend=false" width="600" height="300" frameborder="0"></iframe>

<img src="https://dl.dropboxusercontent.com/u/806656/loadtest22.png">

The above image is a histogram displaying the count of pagehits for all pages 
separated by time period. Depicted are the results from the load tests mentioned above.
This graph is used to help visualize latency as it is easy to visualize which time 
periods had no hits (if there is no bar, there were no hits). Shown below is the 
live graph. 

<iframe src="https://app.datadoghq.com/graph/embed?token=ff5c06d3b0d437235df22cb6c5431e51315ae6d8d5213d28078dc26fcbee912e&height=300&width=600&legend=true" frameborder="0" height="300" width="600"></iframe>


### Level 3

<img src="https://dl.dropboxusercontent.com/u/806656/loadtest3.png"> 

The above image is a histogram displaying the counts of the total pagehits separated by time
period, much like the histogram presented in Level 2. However in this graph, the counts of page hits for 
each individual page are separated by color. The counts for the index page are represented by 
the blue color, and the counts for the add_entry page are represented by the green color. Depicted 
are the results from the load tests mentioned above in level 2. Shown below is the live graph. 

<iframe src="https://app.datadoghq.com/graph/embed?token=fa15793f5c7aba9f0658422db7a7dcdfdda9ad7fc1c985806f05d270236c6d49&height=300&width=600&legend=false" frameborder="0" height="300" width="600"></iframe>

<img src="https://dl.dropboxusercontent.com/u/806656/datadogStackArea.png">

This above image displays the counts of the total pagehits for the add_entry 
page and the index page as stacked areas. The results depicted in this above graph are from a
separate series of load tests that were also simulated as three concurrent 
users randomly visiting the index and add_entry pages with a random delay of up to 10s
between visits. The light gray upper area represents the pagehits for the add_entry page and the dark gray 
lower area represents the pagehits for the index page. Shown below is the live graph. 

<iframe src="https://app.datadoghq.com/graph/embed?token=bd0e53314d4637ef13bfb0f8891dd520fb21575ff021c9bfc6d88b6f3a1c96e2&height=300&width=600&legend=false" frameborder="0" height="300" width="600"></iframe>


### Level 4

<img src="https://dl.dropboxusercontent.com/u/806656/datadog4.png">

For the series of load tests mentioned in Level 2, the above image depicts the overall number of page views 
(for both add_entry and the index page combined) as the yellow line. The number of page views for the add_entry page is depicted as the blue line and the number of page views for the index is depicted as the purple line. Shown below 
is the live graph. 

<iframe src="https://app.datadoghq.com/graph/embed?token=518a191cb8b54178aacd6eb89174357522ab46ee97ec896a8064b0abcb6459f7&height=300&width=600&legend=false" frameborder="0" height="300" width="600"></iframe>

The graphs are likely spikey because of the nature of how dogstatsd aggregates data. 
Because dogstatsd aggregates data by a set time interval (10s by default), the graph
will be spikey because it receives, plots and connects data points as it receives them 
every time interval. 

 
### Level 5

<img src="https://dl.dropboxusercontent.com/u/806656/datadog5.png">

Above is an image of the graph for a metric that randomly samples values between 
0 and 1. Shown below is the live graph. 


<iframe src="https://app.datadoghq.com/graph/embed?token=f2a66b0f48c13cb19b308e6fab4fcee758254745927c9531aaa179cfc706f46d&height=300&width=600&legend=true" frameborder="0" height="300" width="600"></iframe>

The code for the agent check may be found in randomvalcheck.py and randomvalcheck.yaml

### Final Notes

I created a screenboard with the graphs relevant to Levels 2-4 (as well as a few additional
interesting graphs). This screenboard may be found at: https://p.datadoghq.com/sb/06f39eec82

A screenboard with graphs relevant to Level 5 may be found at: https://p.datadoghq.com/sb/4361093a94

If you have any questions or need anything else from me, please email me at 
lwthree@princeton.edu. 
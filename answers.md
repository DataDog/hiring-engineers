Level 1

- Bonus question: what is the agent?

	The agent is softare that collects data from the host to send to Datadog for processing and display.  In this case, the host was my computer, a Mac OS X operating system.  This software can work together with custom event triggers placed into application code that call the Datadog API.

- Submit an event via the API

	See [main.rb](https://github.com/jbmilgrom/hiring-engineers/blob/master/main.rb)

- Get an event to appear in your email inbox (the email address you signed up for the account with)

	See [main.rb](https://github.com/jbmilgrom/hiring-engineers/blob/master/main.rb)

Level 2

-  Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

	I instrumented [LEAf](http://github.com/jbmilgrom/LEAf) with a 'web.page_views' counter.  See this [commit](http://github.com/jbmilgrom/LEAf/commit/c9257f7d85a1a06f989843858322881f212c90be). 

	See this [Datadog post](http://app.datadoghq.com/metric/explorer?from_ts=1407932373348&to_ts=1407935973348&tile_size=m&exp_metric=web.page_views&exp_scope=&exp_group=host&exp_agg=avg&exp_row_type=metric) for a resulting metric.

	Also see [web_page_view.png](http://github.com/jbmilgrom/hiring-engineers/blob/master/web_page_view.png).

-  While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

	I load-tested [LEAf](https://github.com/jbmilgrom/LEAf) using Apache Bench while running a local server (i.e. ab -n 100 -c 2 http://localhost:3000/)
	
	Here is the resulting page-view metric as a [Datadog post](http://app.datadoghq.com/metric/explorer?from_ts=1407932373348&to_ts=1407935973348&tile_size=m&exp_metric=web.page_views&exp_scope=&exp_group=host&exp_agg=avg&exp_row_type=metric). 

	Also see [load_test.png](https://github.com/jbmilgrom/hiring-engineers/blob/master/load_test.png).

-  Create a histogram to see the latency; also give us the link to the graph
	
	I added [this histogram method](https://github.com/jbmilgrom/LEAf/commit/d9188c5633f3442d603956c5c4b27fceb93d6d99) to [LEAf](https://github.com/jbmilgrom/LEAf).  Note that this "latency" test actually tests the latency of the the controller method rendering the html page.  It does not actually test the latency of a completed server html page rendering in response to a corresponding request.
	
	See [histogram.png](https://github.com/jbmilgrom/hiring-engineers/blob/master/histogram.png) for such "latency" results.
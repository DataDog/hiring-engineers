Level 1

- Bonus question: what is the agent?

The agent is softare that collects data from the host to send to Datadog for processing and display.  This software can work alongside custom event triggers placed into application code that interface with the Datadog API.

- Submit an event via the API

See main.rb

- Get an event to appear in your email inbox (the email address you signed up for the account with)

See main.rb

Level 2

-  Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

	I instrumented [LEAf](http://github.com/jbmilgrom/LEAf) with a 'web.page_views' counter.  See this [commit](http://github.com/jbmilgrom/LEAf/commit/c9257f7d85a1a06f989843858322881f212c90be). 

see "https://app.datadoghq.com/metric/explorer?from_ts=1407932373348&to_ts=1407935973348&tile_size=m&exp_metric=web.page_views&exp_scope=&exp_group=host&exp_agg=avg&exp_row_type=metric"

also see web_page_view.png

-  While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

see "https://app.datadoghq.com/metric/explorer?from_ts=1407932373348&to_ts=1407935973348&tile_size=m&exp_metric=web.page_views&exp_scope=&exp_group=host&exp_agg=avg&exp_row_type=metric"

see load_test.png

-  Create a histogram to see the latency; also give us the link to the graph

see histogram.png
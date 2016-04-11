# Level 1

* Sign up for Datadog (use "Datadog Recruiting Candidate" in the "Company" field), get the agent reporting metrics from your local machine.
<img src="img/1-1.png">

* Bonus question: what is the agent?

The agent is the software that runs on the user's computer, monitors the metrics, and sends them to Datadog. It consists of the Collector, Dogstatsd, and the Forwarder.

* Submit an event via the API.

<img src="img/1-2.png">
Code: see level1.rb.

* Get an event to appear in your email inbox (the email address you signed up for the account with)

I tried to do this as follows, but no success yet:
<img src="img/1-4.png">


# Level 2

* Take a simple web app (in any of our supported languages) that you've already built and instrument your code with dogstatsd. This will create metrics.

My app is a Rails app, so I first added the appropriate gem to my Gemfile:

gem 'dogstatsd-ruby'

Next I added code to my sessions controller, so it would run whenever the home page is hit:

    class SessionsController < ApplicationController

      def new
        require 'statsd'
        statsd = Statsd.new
        statsd.increment('web.page_views')
      end



* While running a load test (see References) for a few minutes, visualize page views per second. Send us the link to this graph!

I ran a load test on my app locally with the following command:

ab -n 10000 -c 10 http://127.0.0.1:3000/

Here is the resulting graph: https://p.datadoghq.com/sb/1a534df4e-6235422a4d
<img src="img/1-3.png">

* Create a histogram to see the latency; also give us the link to the graph

* Bonus points for putting together more creative dashboards.

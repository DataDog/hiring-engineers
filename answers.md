## Level 1

#### Sign up for Datadog, get the agent reporting metrics from your local machine.

After signing up and generating an API Key, I installed the Agent via the terminal using:

    <DD_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/setup_agent.sh)"

#### Bonus question: what is the agent?

The Datadog Agent is piece of software that runs on your hosts. Its job is to faithfully collect events and metrics and bring them to Datadog on your behalf so that you can do something useful with your monitoring and performance data.

The Agent has three main parts: the collector, dogstatsd, and the forwarder.

* The collector runs checks on the current machine for whatever integrations you have and it will capture system metrics like memory and CPU.
* Dogstatsd is a statsd backend server you can send custom metrics to from an application.
* The forwader is pushed data from both dogstatsd and the collector and queues it up to be sent to Datadog.

#### Submit an event via the API.

in file 'datadog_event.rb' I write:

    # Load the dogstats module.
    require 'statsd'
    
    # Create a stats instance.
    statsd = Statsd.new('localhost', 8125)
    
    # Submit an event via the API, @mention desired e-mail (be sure e-mail subscription is enabled)
    statsd.event('Good work!', 'You submitted and event via the API. @Jeremy.Salig@gmail.com')

To send an event via the API I run:

    ruby datadog_event.rb.rb

The event will post to my stream and the @mention will forward the event to my e-mail.

#### Get an event to appear in your email inbox (the email address you signed up for the account with)

![event_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L1_01.png)
![email_image](https://s3-us-west-2.amazonaws.com/documentationimages/datadog_L1_02.png)


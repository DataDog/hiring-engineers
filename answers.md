### Level 1

* Sign up for Datadog, get the agent reporting metrics from your local machine.

I had a few minutes of trouble after installing the agent - it was installed but not reporting metrics. I was able to uninstall and reinstall it to fix the issue.

![Installed](http://i.imgur.com/0abvaKJ.png "Agent installed")

* Bonus question: what is the agent?

The Datadog agent collects events, metrics, and data from your hosts to make it easy to track, visualize, and monitor your data in a centralized place. There are three main parts to the agent. First, the collector gathers system info, like memory and CPU, on the machine on which the agent is installed. Next, the Dogstatsd is a statsd backend server to which you can send custom metrics from your app. Finally, the forwarder grabs data from both dogstatsd and the collector and queues it to be sent to Datadog.

* Submit an event via the API.

In hello_dog.rb:

```
require 'rubygems'
require 'dogapi'

api_key = "redacted"

dog = Dogapi::Client.new(api_key)

dog.emit_event(Dogapi::Event.new('You have successfully submitted an event via API! @sfdrago@gmail.com', :msg_title => 'API Event'))
```

Run `ruby hello_dog.rb` in terminal

![Event](http://i.imgur.com/KmZtIuC.png "Event via Api")

* Get an event to appear in your email inbox (the email address you signed up for the account with)

![Email](http://i.imgur.com/PC7zQN6.png "Email Mention")
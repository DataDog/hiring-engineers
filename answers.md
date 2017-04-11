1. In your own words, what is the Agent?

The Agent is a daemon, a long-running, non-interactive background process that runs on your computer (host). The Agent's task can be broken down into three parts: collector, dogstatsd, and the forwarder. The collector runs checks and captures metrics on the current machine for your integrations, while the dogstatsd aggregates your application's metrics, and queues it up for the forwarder to send to Datadog.

Since daemon tasks are typically denoted with a 'd' (e.g. 'sysmond', 'statsd'), you can see it running in your CPU.

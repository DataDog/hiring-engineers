Level 1;

1.Signed up for Datadog

2.What is Datadog ?

The Datadog Agent is piece of software that runs on the client's hosts. 
Its job is to faithfully collect events and metrics and bring them to Datadog on the client's behalf so that the client can do 
something useful with his monitoring and performance data.

The Agent has three main parts: the collector, dogstatsd, and the forwarder.

The collector runs checks on the current machine for whatever integrations the client havs and it will capture system metrics like memory and CPU.
Dogstatsd is a statsd backend server the client can send custom metrics to from an application.
The forwarder retrieves data from both dogstatsd and the collector and then queues it up to be sent to Datadog.
This is all controlled by one supervisor process. This is separate so that the client doesn't have to have the overhead of each application if he doesn't want to run all parts.

3. Event submitted via the API

4. Event appeared on my email viettuan@buffalo.edu

Level 2;




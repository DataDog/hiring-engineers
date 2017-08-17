Bonus question: In your own words, what is the Agent?

The Datadog agent is software that is deployed onto an operating system for the purpose of conducting system, network and application monitoring functions.  With the Datadog agent installed onto each of your systems, you can grain granular insights into the underlying performance + availability of your hosts/systems in both a proactive and reactive manner for optimizing application delivery.

Because the Datadog agent has access to the local OS, it is able to provide a detailed view of the system.   Additionally, as the agent is onboard the host, there is no loss of data when the agent loses connectivity to Datadog.  The agent is also lightweight in its CPU/memory/disk footprint, while also offering action / command based capabilities in addition to the aforementioned data collection features (i.e. restart a process, reboot, etc.).

Some organizations may be “anti-agent” for any number of reasons.  Datadog understands this is the case for some environments, and as a result, an agent-optional approach can be taken whereby only a single Datadog agent needs to be deployed, from which remote monitoring metrics can be collected.    Some examples of elements where remote data collection is applicable include the monitoring of hypervisors, network devices, databases and cloud environments where agents are optional.

To summarize, by strategically deploying Datadog agents across your environment, you can easily monitor local or remote systems, making this architecture ideal for managing cloud or hybrid infrastructures.

A high level architecture diagram can be found here:  https://www.dropbox.com/s/5iw6c38slr3g6ai/Screenshot%202017-08-15%2022.39.36.png?dl=0

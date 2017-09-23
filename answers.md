NOTE: All screenshots contained in screenshots.doc
==================================================

Level 0 Setup

I did the following:
* installed a new version of VirtualBox
* Installed Vagrant
* Installed the Ubuntu VM


Level 1 Collecting Data

I installed and started the agent on the Ubuntu VM.  Note: I had recently downloaded and installed the agent directly to my Mac.  That agent was still running, and I believe it interfered with the new agent on the Ubuntu VM.  When I shut down the Mac agent, the Ubuntu agent started reporting metrics.

What is an agent?
A piece of software that lives on or in some target and performs some local functions in a distributed system.  The functions are organized in and controlled from a central entity.

In the case of Datadog, the functions are about performance monitoring.  The agent retrieves desired data from some system target and sends it to a central server.  Depending on the nature of the agent and the target, the agent may live inside the target (as for example an app agent), live on the target (as for example a host agent), or connect to the target remotely (as for example a database integration).  In all cases, the agent retrieves the desired metrics on a regular schedule and sends them to the central destination.

I located and edited datadog.conf with three tags: os:ubuntu, host:mac, context:lab.



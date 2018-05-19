As an introduction, I am an Enterprise SE with extensive experience evangalizing Networking, Storage and Data Protection solutions.  This has been an intriguring exercise. In my career I have been a consumer of monitoring and analytics, not necessarily involved in the  dev/ops underpinnings that enable them other than providing feedback or feature requests.

I created the environment for this exercise by spinning up a Centos 7 VM in a virutal machine on a local hypervisor. I installed the agent for Centos and verified it was operational see agent_status_before_MongoDB.txt in this branch



Q: Can you change the collection interval without modifying the Python check file you created?
Y: The collection interval is changed in the yaml file for the python check, no in the python check file itself.  Also collection interval for the agent itself, via the metadata providers interval, can be changed.


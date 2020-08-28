### Prerequisites - Setting up the Environment

My Datadog environment setup includes an agent install on my laptop Windows OS and a Ubuntu Linux VM via Vagrant. The setup directions mention that any OS can be used, but having never worked with Vagrant before, I didn't want to pass up an opportunity to challenge myself and learn something new. (It was certainly also a backup in case I really did run into dependency issues--best to be prepared!) 

Upon downloading the Datadog Agent on my local host, I'm now able to browse to http://127.0.0.1:5002/ where I can view my connection as well as other agent info. I can also restart my connection to the agent from this UI. Neat!

![Agent Manager](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/agent_manager.PNG "Agent Manager")

Here's my agent manager, up and running. 

### Collecting Metrics

Agent configuration occurs in the datadog.yaml file, which is my first stop in the tagging task. On my Windows OS, I'm navigating to C:\ProgramData\Datadog, and in my Linux VM, I'm navigating to /etc/datadog-agent/. 

Within datadog.yaml, there's a section labeled tags to which I add a variety of host tags. 

![Windows datadog.yaml File](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/windows_tags_config.PNG "Windows datadog.yaml")
![Linux datadog.yaml File](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/ubuntu_tags_config.PNG "Linux datadog.yaml")

Once the tags are added, the file gets saved, and the agent service is restarted. After 15-30 minutes, the newly-added tags appear in the host info section within the host map. 

![Host Map](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/host_map_windows_tags.PNG "Windows Host Map - Tags")
![Host Map](https://raw.githubusercontent.com/ehuang930/datadog_screenshots/master/host_map_vagrant_tags.PNG "Vagrant Host Map - Tags")

Once I was able to validate that tags were being populated after a config edit in the VM, I proceeded through the rest of the assessment on my Windows OS. 



### Visualizing Data

### Monitoring Data

### Collecting APM Data

### Final Question

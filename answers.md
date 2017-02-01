## Level 0 (optional) - Setup an Ubuntu VM

I installed Vagrant and Virtual Box and very quickly, following the documentation, was able to spin up a Vagrant server `vagrant up` followed by `vagrant ssh` running on Ubuntu 12.04

![vagrant](https://cloud.githubusercontent.com/assets/13028695/22488518/7ceec406-e7e0-11e6-93de-772d284c6342.png)


## Level 1 - Collecting your Data

Having signed up for Datadog, I very quickly installed the Agent, following the one-step installation, on my VM and got it up and running, reporting metrics from my local machine. 


####Bonus question: In your own words, what is the Agent?

- The Agent is software that runs on a client's host which is responsible for communicating local metrics to Data Dog's platform to understand performance and potential issues. The Agent is easy to use and allows for integrations ranging from databases like MySQL to applications such as Slack. The Agent is comprised of 3 parts: the collector (which grabs metrics from local machine for integrations), Dogstatsd (which helps combine data into useful, clear metrics over a period of time), and the forwarder (which talks to both the collector and Dogstatsd to compile and queue information to send to the Datadog platform).

In order to edit the Agent config file to add tags, I had to sync folders from my host to the VM by adding the following line in the Vagrantfile:
`config.vm.synced_folder "./dd-agent", "/etc/dd-agent" `

This enabled me to easily open my text editor of choice (I typically use Atom) to quickly add lines of code to the Vagrantfile and Agent files locally to then be "mirrored" on my VM. Having added these lines of code, I added the following to my datadog.conf file to add tags:

```
# Set the host's tags
# tags: mytag, env:prod, role:database
tags: test_tag, env:stage, role:testing, data_dog_test:tags, name:todd
```
Added `postgres.yaml` to the `conf.d` file and got it to report metrics to the Datadog platform:
```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: pass1234
       tags:
            - optional_tag1
            - optional_tag2
```
Updated Host Map:
![screen shot 2017-01-31 at 12 30 16 pm](https://cloud.githubusercontent.com/assets/13028695/22513796/4ac806b4-e86b-11e6-8176-bd58cd3cf4aa.png)

Custom agent check in `conf.d/random.py`, I used the `gauge` method to measure a value over time:
```python
from checks import AgentCheck
import random

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())

```

Configuration file `random.yaml`:
```yaml
init_config:

instances:
    [{}]

```

Running `sudo /etc/init.d/datadog-agent info` to check that integration is working properly: 
![screen shot 2017-01-31 at 12 26 20 pm](https://cloud.githubusercontent.com/assets/13028695/22515124/7276af86-e86f-11e6-8ee4-5a8cb743f12b.png)
![screen shot 2017-01-31 at 12 25 56 pm](https://cloud.githubusercontent.com/assets/13028695/22515145/82ccfa98-e86f-11e6-9325-3585b2ddf3b3.png)

[Link to dashboard](https://app.datadoghq.com/dash/host/265897649?live=true&page=0&is_auto=false&from_ts=1485962899156&to_ts=1485966499156&tile_size=m)
![screen shot 2017-02-01 at 11 29 20 am](https://cloud.githubusercontent.com/assets/13028695/22515825/da5d257e-e871-11e6-9596-e69554d581c2.png)


### Level 2 - Visualizing your Data

Cloned Database Integration Dashboard:
![screen shot 2017-02-01 at 11 34 53 am](https://cloud.githubusercontent.com/assets/13028695/22516051/88a832c2-e872-11e6-82b5-4e9044d4a616.png)


Additional database metrics and `test.support.random` metric from the custom Agent check:
![screen shot 2017-01-31 at 1 55 55 pm](https://cloud.githubusercontent.com/assets/13028695/22516112/c13686d4-e872-11e6-868b-a49d30a7a7ef.png)

Snapshot of `test.support.random` graph with box around a section that shows it going above 0.90:
![screen shot 2017-01-31 at 1 19 08 pm](https://cloud.githubusercontent.com/assets/13028695/22516196/0602c7d2-e873-11e6-973d-25f1f051fa73.png)

Email notification (note: the notifcation did not immediately appear in my email but rather in a summary email of the day's events):
![screen shot 2017-02-01 at 11 42 05 am](https://cloud.githubusercontent.com/assets/13028695/22516349/86dd75a0-e873-11e6-9f7e-1de477cc4f06.png)
 
  * Bonus question: What is the difference between a timeboard and a screenboard?		 
 

Level 3 - Alerting on your Data

`test.support.random` monitor: 
![screen shot 2017-02-01 at 11 55 11 am](https://cloud.githubusercontent.com/assets/13028695/22516925/6d854c52-e875-11e6-9b45-bd8067e698f6.png)

Set up a monitor on this metric that alerts you when it goes above 0.90 at least once during the last 5 minutes:
Bonus points: Make it a multi-alert by host so that you won't have to recreate it if your infrastructure scales up:
![screen shot 2017-02-01 at 11 55 11 am](https://cloud.githubusercontent.com/assets/13028695/22516925/6d854c52-e875-11e6-9b45-bd8067e698f6.png)

![screen shot 2017-01-31 at 1 34 43 pm](https://cloud.githubusercontent.com/assets/13028695/22516976/909c44b6-e875-11e6-8a1c-42c5d90ec689.png)
![screen shot 2017-02-01 at 11 59 52 am](https://cloud.githubusercontent.com/assets/13028695/22517099/04e81886-e876-11e6-93f6-6aaec2bb64eb.png)
![screen shot 2017-02-01 at 12 00 05 pm](https://cloud.githubusercontent.com/assets/13028695/22517098/04e7d7ae-e876-11e6-9650-4b581ac4a91f.png)
Give it a descriptive monitor name and message (it might be worth it to include the link to your previously created dashboard in the message). Make sure that the monitor will notify you via email:
![screen shot 2017-02-01 at 12 03 38 pm](https://cloud.githubusercontent.com/assets/13028695/22517251/8e0751d6-e876-11e6-84c9-328f7210047c.png)

Monitor Email:
![screen shot 2017-02-01 at 12 05 34 pm](https://cloud.githubusercontent.com/assets/13028695/22517359/cdbcf218-e876-11e6-9999-8a6a42e38f72.png)

Downtime Schedule:
![screen shot 2017-01-31 at 1 28 28 pm](https://cloud.githubusercontent.com/assets/13028695/22517414/01b3416c-e877-11e6-8162-76fce69851a0.png)


Downtime Email:

![screen shot 2017-02-01 at 10 24 23 am](https://cloud.githubusercontent.com/assets/13028695/22517388/e5db5e66-e876-11e6-838e-285b7eaa228b.png)

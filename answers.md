
Indira Williams | Solutions Engineer Candidate

## Environment Set-up
1: Download Vagrant (Make sure its the correct version for your operating system)

2: Download VirtualBox

3: Follow the prompts to install both Vagrant & VirtualBox

4: Run the commands to get Vagrant up & running
	$ vagrant init hashicorp/precise64
	$ vagrant up

5: SSH into vagrant VM by running “vagrant ssh” in the command line
(Side note: terminate the VM by typing “vagrant destroy” into the command line)
![set-up-vm screenshot](./images/set-up-vm.png)

6: Sign up for DataDog

7: Install Agent for the proper environment (Ubuntu)

8: Click “Finish” and your "Events" page should look like this:

![events page screenshot](./images/events-page.png)

## Collecting metrics
1: Add tags to config file:

![add tags screenshot](./images/add-tags-to-config.png)

Host map with tags:

![host map screenshot](./images/host-map-with-tags.png)

2: Integrations (I chose Postgres)

3: Create a custom Agent check that submits a metric named my_metric

![custom metric screenshot](./images/create-custom-metric.png)

my_metric screenshot:
![my_metric screenshot](./images/my-metric.png)

Bonus Question: Can you change the collection interval without modifying the Python check file you created?
Answer: Add ‘min_collection_interval’ to yaml file under init_config.

## Visualizing Data
Create dashboard with graphs using API request:

![test timeboard screenshot](./images/test-timeboard.png)

Set time to last 5 mins, take screen shot, send to self using @ notation:

![test timeboard screenshot](./images/test-timeboard-5mins.png)

Sending to self:

![sending to self screenshot](./images/sending-to-self.png)

Bonus Question: What is the Anomaly graph displaying?
Answer: Any unusual activity

## Monitoring Data
1: Create new metric monitor
2: Set Warning & Alerting thresholds
3: Configure notification

Notification Received:
![monitor notification screenshot](./images/monitor-notification.png)

## Collecting APM Data
APM - https://docs.datadoghq.com/tracing/setup/
- Installed the agent
- Installed the `ddtrace` gem into an existing rails application

![tracing agent screenshot](./images/tracing-agent.png)

- Created the initializers/datadog.rb file in the rails project and added the configuration details:
```ruby
 Datadog.configure do |c|
   c.use :rails, service_name: 'booze_app'
  end
```
- Downloaded the tracing agent (https://github.com/DataDog/datadog-trace-agent#run-on-osx)
- Set enabled the APM in datadog.yaml
```yaml
apm_config:
    enabled: true
```
- Started the rails app
- Started the datadog-agent and the tracing agent
- Clicked around the app and saw the tracing logs

APM Services:
![apm services screenshot](./images/apm-services.png)

APM UI (1):
![apm ui screenshot](./images/apm-ui.png)

APM UI (2):
![apm ui screenshot](./images/apm-ui-2.png)

#### Link to GitHub Repo for Rails App used in this section:
https://github.com/iwilliams83/booze_app

## Final Question
Is there anything creative you would use Datadog for?

Answer: Monitoring the lines at my favorite food spots to get an idea of ideal times to get grub.
OR
Monitoring traffic on retailers' websites to see when there's a sale or promo happening.

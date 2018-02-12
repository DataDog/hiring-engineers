# The Exercise

## Prerequisites - Setup the environment

I used a Vagrantfile to spin up a really simple Ubuntu 12.04 VM on my Mac. No further configuration, just the VM.

```
Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "echo Hello"

  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/precise64"
  end
end```

## Collecting metrics

I installed the datadog agent using the step-by-step instructions on the Ubuntu VM.

<img src="https://farm5.staticflickr.com/4628/26347490248_29ca2206e0_k.jpg" width="500" alt="01_datadog_agent">

I added tags to the datadog.config which describe the function and environment of the machine.

<img src="https://farm5.staticflickr.com/4665/26347489648_b40d888355_k.jpg" width="500" alt="02_agent_tags">

I confirmed the agent tags in the UI.

<img src="https://farm5.staticflickr.com/4712/26347489288_135fe81baf_k.jpg" width="500" alt="03_agent_tags">

As next step I installed PostreSQL on the new machine and added the configuration to the datadog agent.

<img src="https://farm5.staticflickr.com/4612/26347489028_337ab353c5_k.jpg" width="500" alt="04_postgres_config">

I confirmed that everything is runnig using the datadog agent info.

<img src="https://farm5.staticflickr.com/4652/40219952501_4294d56063_k.jpg" width="500" alt="05_postgres_info">

I also checked the UI for the new check.

<img src="https://farm5.staticflickr.com/4619/26347488688_58c6e171fb_k.jpg" width="500" alt="06_postgres_UI">

After the successful PostgreSQL configuration I added the custom metric which I named "fakemetric" instead of "my_metric".

<img src="https://farm5.staticflickr.com/4609/40219952061_1c16909c89_k.jpg" width="500"  alt="07_fakemetric">

After that I set the interval to the minimum of 45.

<img src="https://farm5.staticflickr.com/4623/40219951861_3e5299158a_k.jpg" width="500" alt="08_fakemetric_interval">

I checked that my fakemetric is running successful after restarting the datadog agent.

<img src="https://farm5.staticflickr.com/4767/26347488068_e35f6f2e4c_k.jpg" width="500"  alt="09_fakemetric_info">

**Bonus question**

You can als change the interval in the UI using the metrics configuration.

<img src="https://farm5.staticflickr.com/4757/40219951451_01800ed696_k.jpg" width="500"  alt="10_fakemetric_interval_UI">

## Visualizing Data

I created a new timeboard using python and the datadog module which I installed on my Mac. The code is uploaded in ```datadog_test.py``` as part of this repository.

<img src="https://farm5.staticflickr.com/4657/40219951031_2822dfd166_k.jpg" width="500"  alt="11_api_timeboard">

I checked the Anaomalies graph and reduced it to a 5 minutes view and send it to myself.

<img src="https://farm5.staticflickr.com/4619/40219950311_14760dccfe_h.jpg" width="500" alt="13_anomalies_screenshot_email">

**Bonus Question: What is the Anomaly graph displaying?**

The graph is showing the transactions per second and marks the anaomalies red. It also shows a pretty uniform high and low period.

## Monitoring Data

I created a monitor with the necessary values and used the awesome notification auto-complete feature to create alarm messages per event.

<img src="https://farm5.staticflickr.com/4769/40219950731_86d574a26f_h.jpg" width="500"  alt="12_monitor_alerting">

After a sfew seconds I received an email notification showing that a warning treshold (500) was reached.

<img src="https://farm5.staticflickr.com/4719/40219949901_b91c33e26a_h.jpg" width="500"  alt="14_monitor_alert">

**Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office.**

After that I scheduled two downtimes for the nights on weekdays:

<img src="https://farm5.staticflickr.com/4768/40219949521_7d052fa307_h.jpg" width="500"  alt="15_scheduler_weekdays">

and the weekends:

<img src="https://farm5.staticflickr.com/4703/40219949271_eea03aae8d_h.jpg" width="500"  alt="16_scheduler_weekends">


## Collecting APM Data

I used the given Flask web application to connect the APM solution and check the traces.

<img src="https://farm5.staticflickr.com/4658/40219949091_5386a5003b_h.jpg" width="500"  alt="17_flask_traces">

Finally I created a aggregated dashboard for everything.

<img src="https://farm5.staticflickr.com/4696/40187327572_fd2105537d_h.jpg" width="500"  alt="18_aggregated_dashboard">

**Bonus Question: What is the difference between a Service and a Resource?**

A service describes a set of processes  that´s used (flask in this example) and allows to quickly distinguish between the different processes.

A resource is a particular query to a service. In the flask example it's the requested URI like /api/apm or /trace. So it's more one specific part of a service that is checked.

Reference: https://docs.datadoghq.com/tracing/faq/what-is-the-difference-between-type-service-resource-and-name/


## Final Question

Since there is a datadog agent installed on all machines I would love to scan for security issues and new vulnerabilites to ensure that the compliance can be monitored as well. Maybe intrusion detection can be a good additional feature for companies and administrators as they are already aware of the running services on a machine. 

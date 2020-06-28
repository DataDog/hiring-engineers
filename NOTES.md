# Datadog Hiring Exercise Notes
## Candidate: Sean Carolan

### A Repeatable Lab Environment
**Goal:** Create a repeatable lab environment where I could experiment and learn from the tech exercise. The lab environment should double as a technical demo or tutorial for others to use.

Began my hiring exercise by cloning the git repository into Google Cloud Shell. I chose Google Cloud Platform for my virtual machine because it's fast and easy to work with.

Next, I wrote Terraform code to automate the creation of a VM and the scaffolding required to support it. My first goal was to build a repeatable development environment that would be easy to stand up and tear down.

I used the Terraform file and remote_exec provisioners to download and install the Datadog agent, and to render the /etc/datadog-agent/datadog.yaml configuration file. Once I had my VM up and runnning and registered with Datadog, I added the GCP integration using the Datadog Terraform provider:

https://www.terraform.io/docs/providers/datadog/r/integration_gcp.html

The provider requires sensitive data to work, I opted to use an external data source to avoid exposing the Google credentials or accidentally copying them to GitHub. The Terraform code is designed to read all secrets from environment variables. A service account with viewer access was created for Datadog to use in this integration.

Cleaned up my Terraform code and built a Google Cloud Shell tutorial. Now other users can walk through the same steps I used to set everything up in their own GCP accounts. One of the best ways to learn something is to teach it to others.

**Lessons learned:** The Datadog agent is easy to install and the entire process can be automated using Infrastructure as Code tools like shell scripts, Chef/Puppet/Ansible, or Terraform.

### Observations and Issues
**Goal:** Document anything else I encountered that was interesting or odd.

#### Adding Tags - issue with GCP
I attempted to add tags to my instance using the datadog.yaml file and the example on your tutorial here:

https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments#configuration-files

After several attempts to restart the agent, tear down and rebuild my VM, check my syntax over and over, I decided to try installing the agent on an AWS instance instead. I also tested the configuration on an Azure VM. I observed that an identical datadog.yaml file produces different results on GCP than it does on the other cloud platforms. Azure and AWS instances got tagged just fine, whereas the GCP one never got my custom tags. I used Ubuntu 18.04 on all three VMs.

Full disclosure: I opened a support ticket to report the issue with the GCP instance tags. Todd Rizley informed me that they would be unable to help me with the hiring exercise which is totally fair. I told Todd I'd document my findings and report them during my interview.

To work around this I added tags in the GCP instance metadata in my Terraform code.

I found one issue that may be related about quoting tags. I didn't find any open issues about this agent on GCP, with Ubuntu 18.04.

https://github.com/DataDog/datadog-agent/issues/4982

#### Duplicate host when GCP integration is installed
One issue I encountered was that if you install the GCP integration and the agent, the instance shows up twice in the Datadog inventory. Something's causing it to be registered as two separate hosts. The host that was picked up by the integration does not show an availability zone and the hostname is different:

Picked up by GCP integration:
astro.datadog-gcp-test-2881

Added from the Datadog agent:
astro.us-central1-a.c.datadog-gcp-test-2881.internal

Oddly the agent did register the alias for the machine so I'm not sure why Datadog is unable to map these two together into one host. Perhaps a bug?

UPDATE: After about 25 minutes or so the two machines merged into a single host.

#### Initial impressions on the dashboards
My newly minted host starts out with a bright red color. This doesn't feel right. A new Linux instance should show up 'healthy' or 'green'. I looked closer and it appears that the dashboard has auto-calculated the 'high water mark' for CPU at 0.5%. I adjusted this up to 100% to get my host green.

After a teardown and rebuild of my infrastructure using Terraform I noticed that my host was not showing up in the Datadog console anymore. The agent is running and it says the API key is valid, so not sure what's causing this inconsistency. I'm going to give it 30 minutes and see if my host ever 'checks in'.

```
  API Keys status
  ===============
    API key ending with a9601: API Key valid
```

It's definitely sending data:

```
2020-06-28 17:42:15 UTC | CORE | INFO | (pkg/forwarder/transaction.go:272 in internalProcess) | Successfully posted payload to "https://7-20-2-app.agent.datadoghq.com/intake/?api_key=*************************a9601", the agent will only log transaction success every 500 transactions
```

Finally...after nearly 30 minutes the host showed up on the map. Curious why it may take so long to start registering data?

#### Working with the PostgreSQL integration
No problems installing Postgres and the Postgres integration. I didn't realize at first that I also had to go into the GUI to enable the integration and see it on the dashboard list. The Terraform provider only covers a small handful of integrations for automated installation:
https://www.terraform.io/docs/providers/datadog/index.html

The docs here were not clear about where the postgres.d/conf.yaml file goes:
https://docs.datadoghq.com/integrations/postgres/#installation

This tutorial might be updated to include the full path to the configuration file. New users might not be aware that it is /etc/datadog-agent/conf.d/postgres.d/conf.yaml.

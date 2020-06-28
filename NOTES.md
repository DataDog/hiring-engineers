# Datadog Hiring Exercise Notes
## Candidate: Sean Carolan

Began my hiring exercise by cloning the git repository into Google Cloud Shell. I chose Google Cloud Platform for my virtual machine because it's fast and easy to work with.

Next, I wrote Terraform code to automate the creation of a VM and the scaffolding required to support it. My first goal was to build a repeatable development environment that would be easy to stand up and tear down.

I used the Terraform file and remote_exec provisioners to download and install the Datadog agent, and to render the /etc/datadog/datadog.yaml configuration file. Once I had my VM up and runnning and registered with Datadog, I added the GCP integration using the Datadog Terraform provider:

https://www.terraform.io/docs/providers/datadog/r/integration_gcp.html

The provider requires sensitive data to work, I opted to use an external data source to avoid exposing the google credentials or accidentally copying them to GitHub. The Terraform code is designed to read all secrets from environment variables. A service account with viewer access was created for Datadog to use in this integration.

At this point I attempted to add tags to my instance using the datadog.yaml file and the example on your tutorial here:

https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments#configuration-files

After several attempts to restart the agent, tear down and rebuild my VM, check my syntax over and over, I decided to try installing the agent on an AWS instance instead. I also tested the configuration on an Azure VM. I discovered that an identical datadog.yaml file produces different results on GCP than it does on the other cloud platforms. Azure and AWS instances got tagged just fine, whereas the GCP one never got my custom tags. I used Ubuntu 18.04 on all three VMs.

Full disclosure:  I opened a support ticket to report the issue with the GCP instance tags. Todd Rizley informed me that they would be unable to help me with the hiring exercise which is totally fair. I told Todd I'd document my findings and report them during my interview.

I worked around this on GCP by simply adding tags to the GCP metadata in my terraform, which the agent picks up just fine.

Cleaned up my terraform code and started to build out a Google Cloud Shell tutorial. Now other users can walk through the same steps I used to set everything up in their own GCP accounts.

One issue I encountered was that if you install the GCP integration and the agent, the instance shows up twice in the Datadog inventory. Something's causing it to be registered as two separate hosts. The host that was picked up by the integration does not show an availability zone and the hostname is different:

Picked up by GCP integration:
astro.datadog-gcp-test-2881

Added from the Datadog agent:
astro.us-central1-a.c.datadog-gcp-test-2881.internal

Oddly the agent did register the alias for the machine so I'm not sure why Datadog is unable to map these two together into one host. Perhaps a bug?

UPDATE: After about 25 minutes or so the two machines merged into a single host.

Forcing the hostname as suggested in the documentation doesn't seem to work either:

```
## @param hostname - string - optional - default: auto-detected
## Force the hostname name.
#
# hostname: <HOSTNAME_NAME>
```

I tried this but the auto-generated hostname stays in the dashboard. I also attempted to hard-code the hostname as 'fred' in the datadog.yaml file but it had no effect, the status command shows the hostname remains the same.

```
  Hostnames
  =========
    host_aliases: [astro.datadog-gcp-test-2881]
    hostname: astro.us-central1-a.c.datadog-gcp-test-2881.internal
    socket-fqdn: astro.us-central1-a.c.datadog-gcp-test-2881.internal.
    socket-hostname: astro
```

https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments#host-tags

The duplicate host issue seems to have resolved itself. 

Initial impressions on the dashboards.

My newly minted host starts out with a bright red color. This doesn't feel right. A new Linux instance should show up 'healthy' or 'green'. I looked closer and it appears that the dashboard has auto-calculated the 'high water mark' for CPU at 0.5%. I adjusted this up to 100% to get my host green.





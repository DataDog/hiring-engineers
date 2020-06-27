# Datadog Hiring Exercise Notes
## Candidate: Sean Carolan

Began my hiring exercise by cloning the git repository into Google Cloud Shell.

I chose Google Cloud Platform for my virtual machine because it's fast and easy to work with.

Next, I wrote Terraform code to automate the creation of a VM and the scaffolding required to support it. My first goal was to build a repeatable development environment that would be easy to stand up and tear down.

I used the Terraform file and remote_exec provisioners to download and install the Datadog agent, and to render the /etc/datadog/datadog.yaml configuration file. Once I had my VM up and runnning and registered with Datadog, I added the GCP integration using the Datadog Terraform provider:

https://www.terraform.io/docs/providers/datadog/r/integration_gcp.html

The provider requires sensitive data to work, I opted to use an external data source to avoid exposing the google credentials or accidentally copying them to GitHub. The Terraform code is designed to read all secrets from environment variables.

At this point I attempted to add tags to my instance using the datadog.yaml file and the example on your tutorial here:
https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments#configuration-files

After several attempts to restart the agent, tear down and rebuild my VM, check my syntax over and over, I decided to try installing the agent on an AWS instance instead. I also tested the configuration on an Azure VM. I discovered that an identical datadog.yaml file produces different results on GCP than it does on the other cloud platforms. Azure and AWS instances got tagged just fine, whereas the GCP one never got my custom tags. I used Ubuntu 18.04 on all three VMs.

Full disclosure:  I opened a support ticket to report the issue with the GCP instance tags. Todd Rizley informed me that they would be unable to help me with the hiring exercise which is totally fair. I told Todd I'd document my findings and report them during my interview.

I worked around this on GCP by simply adding tags to the GCP metadata in my terraform, which the agent picks up just fine.

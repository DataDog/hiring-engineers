# Monitor Google Cloud Platform with Datadog

## Getting Started
This guide will walk you through deploying the Datadog agent onto a Google Compute Instance. You'll configure agent settings to collect some metrics, visualize your data with dashboards, monitor the data and send alerts, and configure Datadog to collect application performance data. Let's get started! 🐶

**Time to complete**: About 60 minutes

Click the **Start** button to move to the next step.

## What is Datadog?
Datadog is an infrastructure monitoring SaaS platform.

## Create a Google Cloud Project
You can use an existing Google Cloud Project or create a new one. The project menu is right at the top of your Google Cloud Platform dashboard:

[https://console.cloud.google.com/home/dashboard](https://console.cloud.google.com/home/dashboard)

Once you have created a project (or selected an existing one), you'll need to enable the Compute Engine API. Visit the APIs dashboard and click on the `+Enable APIs and Services` button. Search for 'compute' and select the **Compute Engine API**. Click on the blue **Enable** button.

[https://console.cloud.google.com/apis/dashboard](https://console.cloud.google.com/apis/dashboard)

Click **Next** to proceed.

## Next Step here
More instructions here.

## Another step here
Do some things

```bash
service datadog-agent restart
```

Click **Next** to proceed.

## Terraform Destroy
All done? You can clean up everything you built with the `terraform destroy` command. Try it now:

```bash
terraform destroy
```

You'll need to confirm your intention by typing `yes` again. This is to help prevent accidental deletion of important infrastructure!

Nice work. If you'd like to learn more about Datadog visit the following link:

https://www.datadoghq.com
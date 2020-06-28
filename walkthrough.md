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

You can also easily create a new project using the command line. You may need to add some numbers to the end of your project id if it is already taken. Here we use the built-in $RANDOM variable to accomplish this.

Example:
```bash
export RANDOM_ID=$RANDOM
```

```bash
gcloud projects create datadog-gcp-test-$RANDOM_ID --name="Datadog test project"
```

## Enable the Compute Engine API
Once you have created a project (or selected an existing one), you'll need to enable the Compute Engine API.

Note: You'll require a valid billing account to do the next steps. You can use free Google Cloud credits for this tutorial as long as you have a valid billing account.

Visit the APIs dashboard and click on the `+Enable APIs and Services` button. Search for 'compute' and select the **Compute Engine API**. Click on the blue **Enable** button.

[https://console.cloud.google.com/apis/dashboard](https://console.cloud.google.com/apis/dashboard)

Alternatively you can easily enable the API on the command line. The commands below can be copied and pasted into your Google Cloud Shell terminal.

Set your project ID:
```bash
gcloud config set project datadog-gcp-test-$RANDOM_ID
```

See what billing accounts you have available:
```bash
gcloud beta billing accounts list
```

Link up billing for your project. Replace the billing account ID with your own.
```bash
gcloud beta billing projects link datadog-gcp-test-$RANDOM_ID --billing-account=01234A-FGHIJ7-MNOPQ8
```

Enable the compute engine API:
```bash
gcloud services enable compute
```

Note: You may need to get an administrator to enable billing if your account does not have the correct privileges.

You can verify that the Compute Engine API is enabled with this command:
```bash
gcloud services list | grep compute
```

Click **Next** to proceed.

## Create a Service Account
In order to use the Datadog integration for GCP you'll need to create a service account with viewer access.

Create a service account with the following command:
```bash
gcloud iam service-accounts create datadog-service-account --display-name "Datadog Service Account"
```

Now grant the Viewer role to your new service account:
```bash
gcloud projects add-iam-policy-binding datadog-gcp-test-$RANDOM_ID --member=serviceAccount:datadog-service-account@datadog-gcp-test-$RANDOM_ID.iam.gserviceaccount.com --role=roles/viewer
```

Create a JSON key file for your new service account.
```bash
gcloud iam service-accounts keys create --iam-account datadog-service-account@datadog-gcp-test-$RANDOM_ID.iam.gserviceaccount.com ~/datadog.json
```

Now you should have a Google Cloud credentials file in your home directory called `datadog.json`. We'll use these credentials in the next steps.

## Set up Your Environment Variables
In order to configure your GCP instance and integration you'll need two environment variables, namely `DD_API_KEY` and `DATADOG_GCP_CREDENTIALS`. You can get your Datadog API key at the following URL:

https://app.datadoghq.com/account/settings#api

Copy the API key and run the following commands:

```bash
export DD_API_KEY=YOURAPIKEYHERE
export DATADOG_GCP_CREDENTIALS=$(cat ~/.datadog.json)
```

Check your work by echoing out these variables:

```bash
echo $DD_API_KEY
```

```bash
echo $DATADOG_GCP_CREDENTIALS
```

Ready to start building? Click **Next** to proceed.

## Next Step here
More instructions here.

Click **Next** to proceed.

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
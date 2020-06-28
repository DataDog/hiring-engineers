# Monitor Google Cloud Platform with Datadog

## Getting Started
This guide will walk you through deploying the Datadog agent onto a Google Compute Instance and  configuring the Datadog GCP integration. We'll be using the open source Terraform tool to provision everything from scratch. If you don't know Terraform that's OK, all the required code is already written for you.

Once we have our infrastructure up and running, you'll configure agent settings to collect some metrics, visualize your data with dashboards, monitor the data and send alerts, and configure Datadog to collect application performance data.

Let's get started! 🐶

**Time to complete**: About 60 minutes

Click the **Start** button to move to the next step.

## What is Datadog?
Datadog is an infrastructure monitoring SaaS platform.

## Create a Google Cloud Project
You can use an existing Google Cloud Project or create a new one. The project menu is right at the top of your Google Cloud Platform dashboard:

[https://console.cloud.google.com/home/dashboard](https://console.cloud.google.com/home/dashboard)

You can also easily create a new project using the command line. You may need to add some numbers to the end of your project id if it is already taken. You can use the built-in $RANDOM variable to accomplish this. If you already have your a Project ID you want to use, simply replace the part after the equals sign in the next command.

Example:
```bash
export PROJECT_ID=datadog-gcp-test-$RANDOM
```

```bash
gcloud projects create $PROJECT_ID --name="Datadog test project"
```

Good job. Now that you have a project ID and have defined the PROJECT_ID environment variable, you can click **Next** to continue.

## Enable the Compute Engine API
If you have an existing project with billing and the Compute Engine API already enabled you can skip this step.

Note: You'll require a valid billing account to do this tutorial. You can use free Google Cloud credits for this tutorial as long as you have a valid billing account.

The commands below should be copied and pasted into your Google Cloud Shell terminal.

Set your project ID. This is so you don't have to specify it for every command you run in the terminal.
```bash
gcloud config set project $PROJECT_ID
```

See what billing accounts you have available:
```bash
gcloud beta billing accounts list
```

Link up billing for your project. Replace the billing account ID with your own.
```bash
gcloud beta billing projects link $PROJECT_ID --billing-account=CHANGE-THISTO-YOUROWN
```

Enable the compute engine API. This command can take a minute or more to complete.
```bash
gcloud services enable compute
```

Note: You may need to get an administrator to enable billing if your account does not have the correct privileges.

You can verify that the Compute Engine API is enabled with this command. The output should show Compute Engine API is enabled.
```bash
gcloud services list | grep compute
```

Click **Next** to proceed.

## Create a Service Account
In order to use the Datadog integration for GCP you'll need a service account with viewer access. Datadog requires **read** access to the Google Cloud APIs for your project. This is better than using your admin or owner credentials.

Create a service account with the following command:
```bash
gcloud iam service-accounts create datadog-service-account --display-name "Datadog Service Account"
```

Now grant the Viewer role to your new service account:
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:datadog-service-account@$PROJECT_ID.iam.gserviceaccount.com --role=roles/viewer
```

Create a JSON key file for your new service account.
```bash
gcloud iam service-accounts keys create --iam-account datadog-service-account@$PROJECT_ID.iam.gserviceaccount.com ~/datadog.json
```

Now you should have a Google Cloud credentials file in your home directory called `datadog.json`. We'll use these credentials in the next steps.

Note: In a production environment you might store sensitive keys like this in a [password vault](https://www.vaultproject.io/) or other credentials management system. For the purposes of this tutorial, the datadog.json file is fine.

Click **Next** to continue.

## Set up Your Environment Variables
In order to configure your GCP instance and integration you'll need three environment variables, namely `DD_API_KEY`, `DD_APP_KEY`, and `DATADOG_GCP_CREDENTIALS`. Here's what each credential is for:

* DD_API_KEY - Allows the Datadog agent running on your VM to send data into your Datadog account.

* DD_APP_KEY - Allows our Terraform code to programatically configure your Datadog integrations and dashboards.

* DATADOG_GCP_CREDENTIALS - Read only credentials that allows Datadog to harvest rich data from the Google Cloud APIs for your project.

You can find your Datadog API and application keys at the following URL:

[https://app.datadoghq.com/account/settings#api](https://app.datadoghq.com/account/settings#api)

Run the following commands to export your keys and credentials as environment variables. This is safer than storing sensitive information in your code or text files! Don't forget to replace the placeholders with your real keys.

```bash
export DD_API_KEY=YOURAPIKEYHERE
```

```bash
export DD_APP_KEY=YOURAPPKEYHERE
```

```bash
export DATADOG_GCP_CREDENTIALS=$(cat ~/datadog.json)
```

Check your work by echoing out these variables:

```bash
echo $DD_API_KEY
```

```bash
echo $DD_APP_KEY
```

```bash
echo $DATADOG_GCP_CREDENTIALS
```

Ready to start building? Click **Next** to proceed.

## Build the Base Infrastructure
In this step we'll use Terraform to stand up a virtual machine running Ubuntu 20.04. Don't worry if you haven't used Terraform before.

First change into the directory where our Terraform code is stored. This is also known as your Terraform workspace.
```
cd solutions
```

Next, initialize the directory to download any requried providers:
```
terraform init
```

Configure your project ID inside a tfvars file:
```
echo "project_id = \"$PROJECT_ID\"" > terraform.tfvars
```

Your terraform.tfvars file should now contain a single line defining your project_id. Check it to be sure:
```
cat terraform.tfvars
```

Let's do a dry run. We'll pass in our API key as a command line variable so we don't have to hard-code it into a file:
```
terraform plan -var "dd_api_key=$DD_API_KEY"
```

The output will show that there are 7 resources that will be created:
```
Plan: 7 to add, 0 to change, 0 to destroy.
```

The seven things you'll build include a virtual private cloud (VPC), a network subnet, a TLS (SSH) key, a local copy of your private SSH key, a firewall, a Google Compute instance, and the Datadog integration for GCP.

Let's do it for real this time. Run the following command to build your virtual machine and integration. You'll need to confirm the run by typing `yes` after you run this command.
```
terraform apply -var "dd_api_key=$DD_API_KEY"
```

This part will take a few minutes to complete. You can watch the progress of the run in your terminal.

Click **Next** to proceed.

## Connect to your Virtual Machine
You can connect to your new VM using the SSH command. First we'll need to update the permissions on our private SSH key. Connect to your agent by copying these commands from your Terraform output:

Update the permissions on your private key:
```bash
chmod 600 dogkey.pem
```

Connect to your instance with SSH. Use your own IP address here instead of 1.2.3.4.
```bash
ssh -i dogkey.pem ubuntu@1.2.3.4
```

Answer `yes` when you are prompted with this question:
```
Are you sure you want to continue connecting (yes/no)?
```

Great, you've connected to your Linux instance. You should see an ASCII art image of Bits, the Datadog mascot.

## Working with the Datadog agent
The [Datadog agent](https://docs.datadoghq.com/agent/) is software that runs in the background on all the hosts you wish to monitor. We've pre-installed the agent on your virtual machine for you. Let's take a look at the agent config file:
```
sudo cat /etc/datadog-agent/datadog.yaml
```

There is only one required setting in this file, namely `api_key`. You can adjust all kinds of settings inside of this file but the minimum requirement is a single line containing your API key. We'll be adding some things to this file in the next steps.

Start up the Datadog agent with the following command:
```
sudo systemctl start datadog-agent
```

If the command ran successfully it will not create any output. You can check the agent status at any time with the following command:
```
sudo systemctl status datadog-agent
```

Detailed data about your host is now streaming back to your Datadog account. Check out the host map and you should see a new host called `astro` appear on the map. If you renamed your dogname variable it will show up under a different name.

[https://app.datadoghq.com/infrastructure/map](https://app.datadoghq.com/infrastructure/map)

You can also click on your host and visit its dashboard to see detailed stats collected by the Datadog agent.

Note: It can take a few minutes before your host shows up on the map. If your host shows up twice on the map, don't worry. This happens because the GCP integration also detects the instance from the Google Cloud API. Datadog will merge the two hosts together after a few minutes.

Click on the **Next** button to continue.

## Add some Tags
"Tags are a way of adding dimensions to Datadog telemetries so they can be filtered, aggregated, and compared in Datadog visualizations."

[https://docs.datadoghq.com/getting_started/tagging/](https://docs.datadoghq.com/getting_started/tagging/)

Adding tags is easy, and can be done via configuration files, the UI, the API or DogStatsd. Let's update our configuration file to add some tags to our instance.

First gain a root shell so you don't have to type `sudo` before every command:
```bash
sudo /bin/su - root
```

Now run the following block of code to add some tags to your datadog.yaml file:
```bash
cat <<-EOF > /etc/datadog-agent/datadog.yaml
tags:
  - dogname: Astro
  - dogtype: Great Dane
  - dogshow: The Jetsons
EOF

Restart the agent to update your tags.
```bash
systemctl restart datadog-agent
```

Check out your host's Datadog dashboard to see your new tags. Tags are a powerful way to track and create collections of hosts and services.

Click on the **Next** button to continue.

## Install the PostgreSQL database
Let's install a database for Datadog to monitor. We'll be following the instructions here:

[https://docs.datadoghq.com/integrations/postgres/#installation](https://docs.datadoghq.com/integrations/postgres/#installation)

Use this command to install the PostgreSQL database on your host. Make sure you are SSH'd into your target VM and not your Cloud Shell when you run these commands.
```bash
sudo apt -y install postgresql
```

Next open a psql prompt as the postgres user to create an account for Datadog:
```bash
sudo -u postgres psql
```

Within the psql prompt run this command:
```sql
create user datadog with password 'datadog123';
grant pg_monitor to datadog;
```

Exit the psql (postgres) prompt:
```sql
exit
```

Now test your new account to make sure the permissions are correct. You'll need to type in the password we just set after you enter the command.
```bash
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);" \
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

You can escape from the psql output by entering `ZZ` on your keyboard. Nice work.

Click **Next** to continue.

## Configure the Agent for Database Monitoring
Now you can create a new config file to monitor your PostgreSQL database. Run the following commands to populate the /etc/datadog-agent/postgres.d/conf.yaml file.

First gain a root shell so we don't have to type sudo for every command:
```bash
sudo /bin/su - root
```

Next create the postgres.d config directory:
```bash
mkdir -p /etc/datadog-agent/conf.d/postgres.d
```

The cat command below dumps all the configuration into the file for us. Just copy and paste or click the **Copy to Cloud Shell** button to copy it into your terminal.
```bash
cat <<-EOF > /etc/datadog-agent/conf.d/postgres.d/conf.yaml
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: datadog123
EOF
```

Restart the agent to load your new config:
```bash
systemctl restart datadog-agent
```

Run this command a few times to generate some activity on your database:
```bash
sudo -u postgres sh -c "pgbench -i"
```

Now open up the PostgreSQL screenboard. You should start to see database metrics populate the graphs after a few minutes.

[https://app.datadoghq.com/screen/integration/235/postgres---overview](https://app.datadoghq.com/screen/integration/235/postgres---overview)

Click **Next** to continue.

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
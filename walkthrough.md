# Monitor Google Cloud Platform with Datadog

## Getting Started
This guide will walk you through deploying the Datadog agent onto a Google Compute Instance and  configuring the Datadog GCP integration. We'll be using the open source Terraform tool to provision everything from scratch. If you don't know Terraform that's OK, all the required code is already written for you.

Once we have our infrastructure up and running, you'll configure agent settings to collect some metrics, visualize your data with dashboards, monitor the data and send alerts, and configure Datadog to collect application performance data.

On the left side of the screen you'll see a text editor and a Google Cloud Shell console. The code used by this tutorial is stored in the `cloudshell_open/hiring-engineers` directory.

Read the directions in this sidebar carefully and copy the commands for each step into your terminal window.

Ready? Let's get started! 🐶

**Time to complete**: About 90 minutes

Click the **Start** button to move to the next step.

## What is Datadog?
![Bits the Datadog Mascot](https://github.com/scarolan/hiring-engineers/raw/sean-carolan-answers/solution/assets/dd_logo_v_rgb.png)
<br>

[Datadog](https://www.datadoghq.com) is the essential monitoring platform for cloud applications. We bring together data from servers, containers, databases, and third-party services to make your stack entirely observable. These capabilities help DevOps teams avoid downtime, resolve performance issues, and ensure customers are getting the best user experience.

Click **Next** to continue the tutorial.

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

Set your project ID in your shell environment. This is so you don't have to specify it for every command you run in the terminal.
```bash
gcloud config set project $PROJECT_ID
```

Good job. Now that you have a project ID and have defined the PROJECT_ID environment variable, you can click **Next** to continue.

## Enable the Compute Engine API
If you have an existing project with billing and the Compute Engine API already enabled you can skip this step. Just make sure you have the $PROJECT_ID environment variable set before you move on.

Note: You'll require a valid billing account to do this tutorial. You can use free Google Cloud credits for this tutorial as long as you have a valid billing account.

The commands below should be copied and pasted into your Google Cloud Shell terminal.

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
In this step we'll use Terraform to stand up a virtual machine running Ubuntu 20.04. Don't worry if you haven't used Terraform before, all the commands you need are listed below.

First change into the directory where our Terraform code is stored. This is also known as your Terraform workspace.
```bash
cd solution
```

Next, initialize the workspace to download any requried providers:
```bash
terraform init
```

Configure your project ID inside a tfvars file. The terraform.tfvars file is a convenient place to set non-sensitive variables. You'll have to manually copy and paste this one into the terminal because the auto-copy function doesn't like the escape backslashes. Copy and paste the commend into your shell prompt:
```
echo "project_id = \"$PROJECT_ID\"" > terraform.tfvars
```

Your terraform.tfvars file should now contain a single line defining your project_id. Check it to be sure:
```bash
cat terraform.tfvars
```

Let's do a dry run. We'll pass in our API key as a command line variable so we don't have to hard-code it into a file:
```bash
terraform plan -var "dd_api_key=$DD_API_KEY"
```

The output will show that there are 7 resources that will be created:
```
Plan: 7 to add, 0 to change, 0 to destroy.
```

The seven things you'll build include a virtual private cloud (VPC), a network subnet, a TLS (SSH) key, a local copy of your private SSH key, a firewall, a Google Compute instance, and the Datadog integration for GCP.

Let's do it for real this time. Run the following command to build your virtual machine and integration. You'll need to confirm the run by typing `yes` after you run this command.
```bash
terraform apply -var "dd_api_key=$DD_API_KEY"
```

This part will take a few minutes to complete. You can watch the progress of the run in your terminal. When the Terraform run is complete you'll see some instructions for connecting to your instance.

Click **Next** to proceed.

## View the Google Compute Engine Dashboard
Hop on over to the Datadog Google Compute Dashboard:

[https://app.datadoghq.com/screen/integration/47/google-compute-engine](https://app.datadoghq.com/screen/integration/47/google-compute-engine)

Note that Datadog is already collecting valuable information about your project, even before we've installed or set up any agents. Datadog is using the read-only service account we created earlier to extract data about your project.

Click the little star ⭐ icon to add this dashboard to your Favorites.

In the next step we'll connect to your instance and learn about the Datadog agent.

Click **Next** to continue.

## Connect to your GCP Instance
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

_Are you sure you want to continue connecting (yes/no)?_

Great, you've connected to your Linux instance. You should see an ASCII art image of Bits, the Datadog mascot.

All commands from here on out should be run on your GCP instance, not your Cloud Shell workstation. You can tell which machine you are on by looking at the shell prompt. If your prompt has _cloudshell_ in it you will need to SSH back into your instance. Try typing the hostname command now to make sure you are on the correct machine:

```bash
hostname
```

If you used the default Terraform dogname variable your hostname should be `astro`.

Click **Next** to continue.

## Working with the Datadog agent
The [Datadog agent](https://docs.datadoghq.com/agent/) is software that runs in the background on all the hosts you wish to monitor. We've pre-installed the agent on your virtual machine for you. Let's take a look at the agent config file.

```bash
sudo cat /etc/datadog-agent/datadog.yaml
```

There is only one required setting in this file, namely `api_key`. You can configure many settings in of this file, but the minimum requirement is a single line containing your API key. We'll be adding some things to this file in the next steps.

Start up the Datadog agent with the following command:
```bash
sudo systemctl start datadog-agent
```

If the command ran successfully it will not create any output. You can check the agent status at with the following command:
```bash
sudo systemctl status datadog-agent
```

You should see **active (running)** on the status line. Type `ZZ` to exit if your terminal prompt is missing.

Let's take a closer look at the agent status. Run this command to see more details about all the monitors running on your host:

```bash
sudo datadog-agent status
```

Scroll back through the output and see all the agent settings and default checks. Healthy checks show up with a green `[OK]` next to them.

Detailed data about your host is now streaming back to your Datadog account. Check out the host map and you should see a new host called `astro` appear on the map. If you renamed your dogname variable it will show up under a different name.

[https://app.datadoghq.com/infrastructure/map](https://app.datadoghq.com/infrastructure/map)

You can also click on your host and visit its dashboard to see detailed stats collected by the Datadog agent.

**Note:** It can take a few minutes before your host shows up on the map. If your host shows up twice on the map, don't worry. This happens because the GCP integration also detects the instance from the Google Cloud API. Datadog will merge the two hosts together after a few minutes.

Click on the **Next** button to continue.

## Add some Tags
Tags are a way of adding dimensions to Datadog telemetries so they can be filtered, aggregated, and compared in Datadog visualizations. Tags are always converted to all lower-case, and spaces will be replaced with underscores. You can learn more about tagging in the getting started guide:

[https://docs.datadoghq.com/getting_started/tagging/](https://docs.datadoghq.com/getting_started/tagging/)

Adding tags is easy, and can be done via configuration files, the UI, the API or DogStatsd. Let's update our configuration file to add some tags to our instance.

First gain a root shell so you don't have to type `sudo` before every command:
```bash
sudo /bin/su - root
```

Now run the following block of code to add some tags to your datadog.yaml file. Copy and paste this code into your terminal. This command should only be run once.
```
cat <<-EOF >> /etc/datadog-agent/datadog.yaml
tags:
  - dogname:astro
  - dogtype:great_dane
  - dogshow:the_jetsons
EOF
```

Check out your new datadog.yaml file:
```bash
cat /etc/datadog-agent/datadog.yaml
```

Restart the agent to update your tags.
```bash
systemctl restart datadog-agent
```

Tags are a powerful way to track and create collections of hosts and services. It may take up to ten minutes for the tags to update in the UI. You can proceed with the next steps while the agent runs in the background.

Click on the **Next** button to continue.

## Install the PostgreSQL database
Let's install a database for Datadog to monitor. We'll be following the instructions here:

[https://docs.datadoghq.com/integrations/postgres/#installation](https://docs.datadoghq.com/integrations/postgres/#installation)

You should still be in a root shell. If you don't see a `#` in your prompt run this again:
```bash
sudo /bin/su - root
```

Use this command to install the PostgreSQL database on your host. Make sure you are SSH'd into your target VM and not your Cloud Shell when you run these commands.

First update the apt cache on your host:
```bash
apt -y update
```

Then install the PostgreSQL database package:
```bash
apt -y install postgresql
```

Next open a psql prompt as the postgres user to create an account for Datadog:
```bash
sudo -u postgres psql
```

Within the psql prompt run this command. You'll need to copy and paste this into the terminal. Be sure you hit `ENTER` after the second command.
```sql
create user datadog with password 'datadog123';
grant pg_monitor to datadog;
```

Exit the psql (postgres) prompt:
```bash
exit
```

Now test your new account to make sure the permissions are correct. You'll need to type in the password we just set after you enter the command.
```
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);" \
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

You can escape from the psql output by entering `ZZ` on your keyboard. Nice work.

Click **Next** to continue.

## Configure the Agent for Database Monitoring
Now you can create a new config file to monitor your PostgreSQL database. Run the following commands to populate the /etc/datadog-agent/postgres.d/conf.yaml file.

If you are already in a root prompt (it looks like a `#` symbol), you can skip this step.
```bash
sudo /bin/su - root
```

Next create the postgres.d config directory:
```bash
mkdir -p /etc/datadog-agent/conf.d/postgres.d
```

The cat command below dumps all the configuration into the file for us. You'll need to copy and paste this block of code into your terminal, as the auto-run button won't work here.
```
cat <<-EOF > /etc/datadog-agent/conf.d/postgres.d/conf.yaml
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: datadog123
EOF
```

Restart PostgreSQL to load the new configuration:
```bash
systemctl restart postgresql
```

Restart the datadog agent to load your new config:
```bash
systemctl restart datadog-agent
```

Set up the pgbench tool so we can generate database activity:
```bash
sudo -u postgres sh -c "pgbench -i"
```

Next, run this one liner to start generating connections to your database. It will tie up 5/100 of your available database connections. Leave this script running for a few minutes to generate data for your dashboards. Use `CTRL-C` to stop it when you are done generating traffic.
```bash
while true; do sudo -u postgres sh -c "pgbench -c 5 -C"; sleep 1; done
```

Back in your Datadog account, enable the PostgreSQL integration:
[https://app.datadoghq.com/account/settings#integrations/postgres](https://app.datadoghq.com/account/settings#integrations/postgres)

You'll need to scroll to the bottom of the configuration tab and click on the **Install** button there.

Now open up the PostgreSQL metrics dashboard. You should start to see database metrics populate the graphs after a few minutes.

[https://app.datadoghq.com/dash/integration/17/postgres---metrics](https://app.datadoghq.com/dash/integration/17/postgres---metrics)

Add the Postgres - Metric dashboard to your favorites by clicking on the star ⭐ icon.

Click **Next** to continue.

## Create a Custom Agent Check
In this step we'll add a custom agent check to your instance. Custom agent checks are written in Python and should be stored in `/etc/datadog-agent/checks.d`. Each check should have an identically named yaml configuration file inside `/etc/datadog-agent/conf.d`. You can also store your files in subdirectories for easier organization.

```bash
echo "instances: [{}]" > /etc/datadog-agent/conf.d/random_number.yaml
```

Next, copy the check's Python script into the checks.d directory.
```bash
cp /home/ubuntu/random_number.py /etc/datadog-agent/checks.d/random_number.py
```

Finally restart the agent to start collecting random numbers.
```bash
systemctl restart datadog-agent
```

Your host's Datadog dashboard should now show a new entry called **random_number** under the Apps Running section. Click it to see a graph of all the random numbers that were generated.

Next let's change your collection interval. Overwrite your random_number.yaml file with the following command:
```bash
echo "instances: [{min_collection_interval: 45}]" > /etc/datadog-agent/conf.d/random_number.yaml
```

Restart the agent to activate the new collection interval.
```bash
systemctl restart datadog-agent
```

You should now see data points on the graph showing up roughly 40 seconds apart. The granularity of the graph is measured in 20 second intervals.

Click **Next** to continue.

## Visualizing Monitoring Data
As you've probably guessed, you can create custom dashboards to show all kinds of metrics and alert conditions. When you spun up this lab environment using Terraform a special dashboard was created that includes three widgets on it.

In the **Dashboards** menu click on **Dashboard List**. Next, click on **Datadog Tutorial Dashboard**. This dashboard was created programatically with Terraform code. You can see the code that built the dashboard in the `dd_dashboard.tf` file in the code editor.

Take a closer look at the **PostgreSQL % Max Connections on astro** graph. You should see the database activity you generated earlier with the one-liner.

Back on your VM, run the database benchmark script again, but this time we'll simulate 95 connections instead of 5.

```bash
while true; do sudo -u postgres sh -c "pgbench -c 95 -C"; sleep 1; done
```

Watch the anomaly graph for a few minutes. What happens?

Click **Next** to continue

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
## Prerequisites - Setup the environment

### OS setup
I have used Ubuntu on top of VMware for this. Skipping the walkthrough of that part because we have bigger concern here.

### Datadog agent setup

**Step 1: Account Create**

Setup a free trial account from Datadog site [here]( https://app.datadoghq.com/signup "Datadog signup") and start using 14 days of evaluation.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Datadog_account_page.jpg" />
</div>

**Step 2: Agent Installation**

Now that the account has been created, the first landing page after login to the portal will ask to choose the OS. Select Ubuntu there:
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Datadog_agent_page.jpg" />
</div>

The next page will provide a command to run in the OS:
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Datadog_Ubuntu_agent_page.jpg" />
</div>

```
DD_API_KEY=02f734414a40cee6e9861fa0cee0fb3a bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
Simply run the commad and the agent will be installed automatically.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Agent_ins_start.jpg" />
</div>

Below massage will be shown upon successful installation:
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Agent_ins_fin.jpg" />
</div>

Once completed the Agent status can be seen with the command ``datadog-agent status`` in the command window.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/Agent_status.jpg" />
</div>

### Collecting Metrics:

**1. Add tags**

To add tag we need to edit the ``datadog.yaml`` file under ``/etc/datadog-agent`` which is the default directory of Datadog agent.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/add_tags_yaml.jpg" />
</div>

Simply add the tags in ``key:value`` format.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/host_tags.jpg" />
</div>

Once done, dont forget to restart the agent using commad ``systemctl restart datadog-agent``

Now the freshly added tags are seen in the Datadog Host Map page.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/DD_hostmap_full.jpg" />
</div>

**2. Datadog integration for database**

Fist we need to install postgresql database. Its easy in Ubuntu, just need to run a single commad and sit back.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/postgresql_ins_start.jpg" />
</div>

Once that done, we need to go to Integration page of Datadog site.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/integration.jpg" />
</div>

And find PostgreSQL there. Clicking on it provides us all the commands required to configure agent for the database.
<div align="center">
<img src="https://github.com/Tosrif/Tosrif-hiring-engineers/blob/solutions-engineer/files/DD_postgresql_config.jpg" />
</div>

Login to the postgresql database and run the first SQL there to create datadog user and grant in permission.

```
create user datadog with password 'nD7kgb57p06o34cwTfDV30ww';
grant SELECT ON pg_stat_database to datadog;
```
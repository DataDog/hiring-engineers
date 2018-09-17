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


### Collecting Metrics:



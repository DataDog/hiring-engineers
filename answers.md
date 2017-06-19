
On the Datadog main page, go to the sign up link located on the top right corner of the site. Enter all the required information to create an account. Follow the prompt until the last section which is for setting up an Agent (Datadog Agent). See picture here (001, 002)

Choose the appropriate platform/OS accordingly by hitting the tab on the left pane. Copy and paste the command on to the terminal. You may need to use sudo for the authentication purpose.
See picture here (003, 004)

Bonus Question: What is the Agent?
The Datadog Agent is a software that act on our behalf  in gathering/collecting events and metrics in order to present (monitor) useful data.

Adding tag, [more information on tagging can be found here](http://docs.datadoghq.com/guides/basic_agent_usage/osx/)
See picture here (005)

`/usr/local/bin/datadog-agent start`
`/usr/local/bin/datadog-agent stop`

On the integrations part (located on the left pane), select the application you wish to install(example postgres), under the configuration tab hit the install integration to begin the installation. See picture here (006, 007)

Install postgres on to the local machine. See picture here (008, 009, 010)

Write a custom Agent, create a file example datadog-agent/agent/checks.d/check.py. Create the corrensponde config file (ex. datadog-agent/agent/checks.d/check.yaml)
[See here for guidlines](http://docs.datadoghq.com/guides/agent_checks/)
See picture here (010)

Restart the datadog agent by executing this command 

  `/usr/local/bin/datadog-agent restart`

See picture here (011)


Bonus: What is the difference between a timeboard and a screenboard?
Timeboard are great for troubleshooting and correlation where as sceenboard allows custom drag and drop which is great for display.

On the left panel of the dashboard, find the Infrastructure and click on the Infrastructure List and Host Map to see the matrix. See picture here (012)

On the sidebar of Datadog panel, hover to Monitor section, set up the monitor on this metric;
alert when it goes above 0.90 at least once during the last 5 minutes, on the last section mention user(s) by adding an email adddress/by mentioning the user(s)

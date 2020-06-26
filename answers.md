```       
       .-'`   `'-.
   _,.'.===   ===.'.,_
  / /  .___. .___.  \ \
 / /   ( o ) ( o )   \ \                                            _
: /|    '-'___'-'    |\ ;                                          (_)
| |`\_,.-'`   `"-.,_/'| |                                          /|
| |  \             /  | |                                         /\;
| |   \           /   | | _                              ___     /\/
| |    \   __    /\   | |' `\-.-.-.-.-.-.-.-.-.-.-.-.-./`   `"-,/\/ 
| |     \ (__)  /\ `-'| |    `\ \ \ \ \ \ \ \ \ \ \ \ \`\       \/
| |      \-...-/  `-,_| |      \`\ \ \ \ \ \ \ \ \ \ \ \ \       \
| |       '---'    /  | |       | | | | | | | | | | | | | |       |
| |               |   | |       |    Datadog - Mihai    | |       |
\_/               |   \_/       | | | | | | | | | | | | | | .--.  ;
                  |       .--.  | | | | | | | | | | | | | | |  | /
                   \      |  | / / / / / / / / / / / / / /  |  |/
                   |`-.___|  |/-'-'-'-'-'-'-'-'-'-'-'-'-'`--|  |
            ,.-----'~~;   |  |                  (_(_(______)|  |
           (_(_(_______)  |  |                         ,-----`~~~\
                    ,-----`~~~\                      (_(_(_______)
                   (_(_(_______)

```
# Prerequisites - Setting up the environment

- [x] Spinned up an Azure Ubuntu VM and connected to it.


- [x] Installed a Datadog agent

![prerequisites](screens/screen2.PNG "Prerequisite 1")

# Collecting Metrics

- [x] Edited the datadog.yaml file, added the tags, restarted the Datadog Agent.

![prerequisites](screens/screen4.PNG "Prerequisite 2")

- [x] Installed the MySQL database on the VM, created the datadog database user and gave it the necessary rights according to this integration documentation: https://docs.datadoghq.com/integrations/mysql/ Created a conf.yaml file and updated the necessary configurations. Restarted the MySQL database and the Datadog agent to enable MySQL monitoring.

![prerequisites](screens/screen5.PNG "Prerequisite 4")

- [x] Created a file in conf.d folder named my_metrics.yaml

![prerequisites](screens/screen6.PNG "Prerequisite 4")

- [x] Created a file in checks.d folder named my_metrics.py and added the following code as suggested here: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

![prerequisites](screens/screen7.PNG "Prerequisite 5")

- [x] Restarted the agent after which it was possible to monitor 'my_metrics' using either 'sudo service datadog-agent status' or the Metrics Explorer:

![prerequisites](screens/screen8.PNG "Prerequisite 6")

- [x] Updated the collection interval in the 'my_metrics.yaml' file to submit the metrics once every 45 seconds: 

![prerequisites](screens/screen9.PNG "Prerequisite 7")

**Bonus question**: Yes, it is possible to modify the collection interval without modifying the Python file by modifying the configuration file as it was executed above. The interval modification using the configuration file was inspired by this: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

Bonus Question Can you change the collection interval without modifying the Python check file you created?

# Visualizing Data:

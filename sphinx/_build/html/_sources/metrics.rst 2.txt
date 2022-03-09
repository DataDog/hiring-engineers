Collecting Metrics
==================

Check Status of Agent
---------------------

1. Check status of Datadog Agent
    .. code-block::

        vagrant@vagrant:~$ sudo service datadog-agent status

    .. image:: images/datadog_agent_status.gif
        :align: center

2. Check to see if there is activity being displayed in a web-dashboard

    .. image:: images/system_metrics_web_dashboard.png
        :align: center


\

Adding Host Tags
----------------
There are several ways to setup tags within the Datadog Platform. I decided to set them up via the agent configuration files as guided in the challenge's instructions.

   .. note::
       You can assign tags through the configuration files, the Datadog site (UI), Datadog's API, and DogStatsD

1. Open the Agent's main configuration file

   .. code-block::

       vagrant@vagrant:~$ sudo vim /etc/datadog-agent/datadog.yaml

\

    .. image:: images/datadog.yaml_config_file.gif

 .. note::
     Make sure the API key looks correct and that the agent is pointing to the correct Datadog site

2. I created a custom hostname in this file and set it to: ``hostname:BMELLO``

3. I then added the host tags in the same configuration file

   .. image:: images/datadog_tags.png
        :align: center

\
    .. note::
        Make sure you have the correct indentation in the datadog.yaml (configuration) file. I ran into this issue and the Datadog Agent would not restart.

4. Restart Datadog Agent: ``vagrant@vagrant:~$ sudo service datadog-agent restart``

5. You should now see your host and its' associated tags on the Host Map page in Datadog

   .. image:: images/datadog_host_map_with_tags.png
       :align: center

\
    .. image:: images/tags.png
        :align: center



Database Installation (MySQL)
-----------------------------

1. Install MySQL Server on Ubuntu VM

   .. code-block::

       vagrant@vagrant:~$ sudo apt install mysql-server

\
    .. image:: images/install_mysql.gif
        :align: center

\

2. Configure MySQL \

   - Run the included security script for MySQL as this will change some of the less secure default options for things like remote root logins and sample users. Even though this is a test environment, we do not want it becoming vulnerable running insecure services.

   .. code-block::

       vagrant@vagrant:~$ sudo mysql_secure_installation

\
    .. image:: images/mysql_secure.png
        :align: center

\

    .. note::
        As you can see in the image above, I left the test database in place so I have data to query when instrumenting with Datadog.

\

3. Check Status of MySQL to make sure it is up and running

   .. code-block::

       vagrant@vagrant:~$ sudo service mysql status

\
    .. image:: images/mysql_status.gif
        :align: center

\

Add user to MySQL for Datadog
-----------------------------

\

1. Change to MySQL shell

\
    .. code-block::

        vagrant@vagrant:~$ mysql -u root -p

\
    .. image:: images/mysql_shell.gif
        :align: center


\

2. Add Datadog user

\
    .. code-block:: 

        mysql > CREATE USER 'datadog'@'%' IDENTIFIED BY '<UNIQUEPASSWORD>';

\
    .. image:: images/create_user_mysql.png
        :align: center

\
    .. note::
        Check to see what version of MySQL you are running as the scripts are different for adding a user to Datadog

\
    .. image:: images/mysql_version.png
        :align: center

\

3. Test to make sure user was added successfuly

\
    .. code-block::

        vagrant@vagrant:~$ mysql -u datadog --password=<UNIQUEPASSWORD> -e "show status" | \
        grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
        echo -e "\033[0;31mCannot connect to MySQL\033[0m"

\
    .. image:: images/mysql_user_ok.png
        :align: center

\

4. Add privileges to the user so the Agent can collect metrics

\
    .. code-block::

        mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'%' WITH MAX_USER_CONNECTIONS 5;

\
    .. image:: images/grant_replication_client_mysql.png
        :align: center

\
    .. code-block::

        mysql> GRANT PROCESS ON *.* TO 'datadog'@'%';

\
    .. image:: images/grant_process_on_mysql.png
        :align: center

\

5. To collect additional metrics, enable ``performance_schema``

\

    .. code-block::

        mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'%';

\
    .. image:: images/mysql_performance_schema.png
        :align: center

\

6. Reload the grant tables in the MySQL database so the privilges granted to the user can take effect wihtout reloading or restarting the MySQL service.

\
    .. code-block::

        mysql> FLUSH PRIVILEGES;

\

7. Check to make sure privilges were added to Datadog user

\
    .. code-block:: 

        mysql> show grants for 'datadog'@'%';

\

    .. image:: images/show_grants_user_mysql.png
        :align: center

\

Add MySQL Configuration to Datadog Agent
----------------------------------------

1. Add configuration block to the ``mysql.d/conf.yaml`` file to collect the MySQL metrics

\
    .. code-block::

        vagrant@vagrant:~$ sudo vim /etc/datadog-agent/conf.d/mysql.d/conf.yaml

\
    .. image:: images/mysql.d:conf.png
        :align: center

\
    .. note::
        Wrap your password in single quotes in case a special character is present

\

2. Restart the Agent to start sending MySQL metrics to Datadog:

\
    ``vagrant@vagrant:~$ sudo service datadog-agent restart``

\

3. Make MySQL logs more accessible
   - Edit ``/etc/mysql/conf.d/mysqld_safe_syslog.cnf`` and remove or comment the lines.

\
   - Edit ``/etc/mysql/my.cnf`` and add following lines to enable general, error, and slow query logs

\
    .. code-block::

        [mysqld_safe]
        log_error = /var/log/mysql/mysql_error.log

        [mysqld]
        general_log = on
        general_log_file = /var/log/mysql/mysql.log
        log_error = /var/log/mysql/mysql_error.log
        slow_query_log = on
        slow_query_log_file = /var/log/mysql/mysql_slow.log
        long_query_time = 2

\

4. Restart MySQL: ``sudo service mysql restart``

\

5. Make sure Agent has read access on ``var/log/mysql``

\

6. In ``/etc/logrotate.d/mysql-server`` there should be something similar to:
\

    .. image:: images/:etc:logrotate.d:mysql-server.png
        :align: center

\

7. Enable Log Collection in the Agent's ``datadog.yaml`` file
\

    .. image:: images/logs=enabled_datadog_yaml.png
        :align: center

\

8. Add Configuration block to the ``/etc/datadog-agent/conf.d/mysql.d/conf.yaml`` file to start collecting MySQL logs
\

    .. image:: images/add_logs_configblock_to_confyaml.png
        :align: center

\

9. Restart the Agent: ``vagrant@vagrant:~$ sudo service datadog-agent restart``

\

Check MySQL Integration in Datadog UI
-------------------------------------

1. Datadog UI now recognizes the MySQL Integration
\

    .. image:: images/mysql_integration_installed.png
        :align: center

\

2. The Host Map now shows MySQL with Metrics and a Status Check
\

    .. image:: images/mysql_host_map_metrics.png
        :align: center

\

    .. image:: images/mysql_host_map_statuscheck.png
        :align: center

\

3. MySQL Overview Dashboard
\

    .. image:: images/mysql_overview_dashboard.png
        :align: center

\

Create Custom Agent Check
-------------------------

1. Change to the ``conf.d`` directory of the Datadog Agent and create a new config file for the custom Agent check
\

    ``vagrant@vagrant:~$ sudo vim /etc/datadog-agent/conf.d/custom_my_metric_check.yaml``

\

2. Edit the ``custom_my_metric_check.yaml`` file to include the config
\

    .. image:: images/custom_my_metric_check_yaml.png
        :align: center

\

3. Create a new Python Check file ``my_metric``  in the ``checks.d`` directory of the Agent
\

    ``vagrant@vagrant:~$ sudo vim /etc/datadog-agent/checks.d/custom_my_metric_check.py``

\

    .. image:: images/custom_my_metric_check_py_new.png
        :align: center

\

4. Restart the Agent: ``vagrant@vagrant:~$ sudo service datadog-agent restart``

\

    .. note::
        The names of the configuration and check files must match. If your check is called ``custom_my_metric_check.py`` the configuration file must be name ``custom_my_metric_check.yaml``

\

5. Change back to the ``sudo vim /etc/datadog-agent/conf.d/custom_my_metric_check.yaml`` file and edit the ``min_collection_interval`` to 45 seconds.

\

    .. image:: images/min_collection_interval=45.png
        :align: center

\

6. Verify that your check is running

\

    ``sudo -u dd-agent -- datadog-agent check custom_my_metric_check``

\

    .. image:: images/verifying_custom_check.png
        :align: center

\

7. You will now see the ``my_metric`` graph show up in the Metrics Explorer
\

    .. image:: images/my_metric_explorer.png
        :align: center


\

**Bonus** : It is possible to change the collection interval through the configuration file created in ``/etc/datadog-agent/conf.d/custom_my_metric_check.yaml`` without modifying the python code. This was executed in Step 5 of this section.























































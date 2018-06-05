## Prerequisites - Setup the environment
=======================================

I decided to use Vagrant VM to avoid dependency issues.

![agent reporting metrics](/img/agent_reporting_metrics.png) 

###### Documentation I used to complete this section: 
[Vagrant Setup Documentation](https://www.vagrantup.com/intro/getting-started/project_setup.html)
[Datadog Overview](https://www.youtube.com/watch?v=mpuVItJSFMc)

## Collecting Metrics:
=====================
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

⋅⋅⋅ ![Host Map page showing Tags](/img/hostmap_tag.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

⋅⋅⋅ I use MySQL so that's what I used for this challenge. 
⋅⋅⋅ ![MySQL Integration](/img/mysql_integration.png)



###### Documentation I used to complete this section:
=====================================================
[Datadog Doc - How to use Tags](https://docs.datadoghq.com/getting_started/tagging/using_tags/)
[Datadog Doc - How to assign Tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/)
[Datadog Doc - MySQL Integration ](https://docs.datadoghq.com/integrations/mysql/)

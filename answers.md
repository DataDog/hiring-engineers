Hello!

For the purposes of this exercise, I'll be using Ubuntu 18.04 running on two t2.medium in AWS. I installed the Datadog agent and all related technologies both directly on the host and as dockerized containers.

![Host Map]{https://imgur.com/a/5S39oqe}

<h1> Collecting Metrics <h1>
  
  * On the host install, I passed the following tags in through datadog.yaml:
  
 ![Tags in .yaml]{https://imgur.com/a/T8CYUmd}
 
 They passed into the app successfully!
 
 ![Tags in app]{https://imgur.com/a/daPi4od}
 
  * I decided to use a MySQL database for the Integration demonstration. You can find my MySQL conf file [here](https://github.com/nysyr/hiring-engineers/blob/solutions-engineer/mysql.d/conf.yaml).
 
 After adding the Datadog user and giving it the [necessary permissions in the database](https://github.com/nysyr/hiring-engineers/blob/solutions-engineer/mysql.d/mysqlCommandsExample.txt) I restarted the DD Agent and saw that the check was integrated:
 
![MySQL Check]{https://imgur.com/a/c5dfwHP}

Additionally, I saw metrics flowing into the app for the DB:

![MySQL Metrics]{https://imgur.com/a/RWNVGz0}

 * I then created a rudimentary custom agent check to push a gauge value of 777 and set the interval to 45 seconds in the .yaml file.
   Here it is coming in:
   
   ![my_metric in app]{https://imgur.com/a/o1y6llp}
 
 * Then I changed the interval to 30 seconds in the Metric Summary:
 
 ![Changing the Interval in App]{https://imgur.com/a/LToSIyq}
 
 <h1>Visualizing Data<h1>

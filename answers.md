# datadog tech exercise 


## Prerequisites - Setup the environment

I set up a VPS using Amazon EC2. Ubuntu server.

## Collecting Metrics:

###  Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
- Edit the datadog.yaml file to add some tags
- Datadog install location can found here: https://docs.datadoghq.com/agent/basic_agent_usage

**![](https://lh5.googleusercontent.com/kk9hFEeGs9ABJRzL5eBx4EXG_dVeNw9DsOw5E1tgxvvpHmB4wWlq2xzJ9onEfIhY7YlrgEHCb9Xdok37STe3i48w0I-19CaJB2HM77e56gu8o7uAfjbtxYW2uDSE0pp41xnRMuib)**

Took a while for the stats to propagate to the front end UI:

**![](https://lh5.googleusercontent.com/NiAlf3AgOvtH8Lj67SUaJbhjj0YbfGm-ruAG5fuQt2mSqFK52y44i0xa5hQ1GlUuc2oUpHyhyBRtkzgCopT80Zg6ZRTvSpCqEdYC8uIEBspPID1jkEkjF3pGpjY4O8SFPFWc7GNH)**


## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Install mySQL:


     sudo apt-get update sudo apt-get install mysql-server

start mySQL

    mysql -u root -p

create User

    CREATE USER 'datadog'@'localhost' IDENTIFIED BY '32158oph'

grant permissions as per: https://docs.datadoghq.com/integrations/mysql/

edit mysql conf file as per: [https://docs.datadoghq.com/integrations/mysql/](https://docs.datadoghq.com/integrations/mysql/)

enable logs as per: [https://docs.datadoghq.com/integrations/mysql/](https://docs.datadoghq.com/integrations/mysql/)

mySQL installed, visible in Datadog:
**![](https://lh4.googleusercontent.com/kvcqypmLdTktOC8sdmb8q7W3hPrDkEXlhO12COhzDU0cOZ0gvFKlrzTpiWg2gqEz_tFeOFGFmC84ZGlge7YW991ERVXK5HnEmHblSfYOsL_3kXIv8WYzRknzKmlnpfJ2XmT4uG_F)**

mySQL metrics in Datadog dashboard:
**![](https://lh4.googleusercontent.com/H30JjrlXaSkU9jG3YWo27Kcy1PbzRB5sGDVEteoMe9oe78pCHZbD8JtkbNDkBXS8tGLEqqL1Ss1QvR8ILSzozd359zyDKzrWxO0inEp1DX7I8t8mPWHaLdCuDEZI4oU7oxIke9xg)**

##  Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Create Check and Check conffiguration as per:
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#should-you-write-an-agent-check-or-an-integration

Here is the Check code:

    import random
     
    try:
       from datadog_checks.base import AgentCheck
    except ImportError:
       from checks import AgentCheck
     
    __version__ = "1.0.0"
     
    class HelloCheck(AgentCheck):
       def check(self, instance):
           self.gauge('my_metric', random.randint(1,1001), tags=['author:richard_flynn'])

Check is running OK:
**![](https://lh6.googleusercontent.com/gmuwUe_oNBdDYx131nwKuvUQUQPJVBrQ6CKvQgaAX2M3Xx7ckHZtCopeaRKvoBz1DcZBPmCf4Z4txjMoQq1UEi2U16AgQjblGbvDopXcdsd2hI72jVosymIybPd-7jzE6eZCfla0)**

**Bonus Question Can you change the collection interval without modifying the Python check file you created?**

Yes, using the config file:
**![](https://lh4.googleusercontent.com/n5Cht_9MO6Tpd7jRBZw88opq2CsuPxvbwKJXfdauyWTWhr-vZsWwDcO3WCGIOMJzHVBleE5S_Ylxbfg4dnKD4zLlRpSfK4rf8V2eI6cnNOZD4oPhov780vBw5CsZe2NvMg8efgAZ)**

- change min_collection_interval to 40


##  **Utilize the Datadog API to create a Timeboard**

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard:

    from datadog import initialize, api
     
    print('start')
     
    options = {
       'api_key': 'e48259719e8bcad8f046e307e7295120',
       'app_key':'78ffba202a080e5e42994766946356fbcd805824'
    }
     
    initialize(**options)
     
    title = 'RF custom metrics dash v7 (rollup)'
    widgets = [{
       'definition': {
           'type': 'timeseries',
           'requests': [
               {'q': 'avg:rf.custom.a{*}'}
           ],
           'title': 'custom metric avg'
       }
    },
    {
       'definition': {
           'type': 'query_value',
           'requests': [
               {'q': 'avg:rf.custom.a{*}.rollup(sum,3600)'}
           ],
           'title': 'custom metric rolled up (1 hr)'
       }
    }
     
    ]
    layout_type = 'ordered'
    description = 'A dashboard with memory info.'
    is_read_only = True
    notify_list = ['user@domain.com']
    template_variables = [{
       'name': 'host1',
       'prefix': 'host',
       'default': 'my-host'
    }]
     
    saved_view = [{
       'name': 'Saved views for hostname 2',
       'template_variables': [{'name': 'host', 'value': '<HOSTNAME_2>'}]}
    ]
     
    api.Dashboard.create(title=title,
       widgets=widgets,
       layout_type=layout_type,
       description=description,
       is_read_only=is_read_only,
       notify_list=notify_list,
       template_variables=template_variables,
       template_variable_presets=saved_view)
     
    print('fin')


Custom Metrics:
**![](https://lh4.googleusercontent.com/EYedIsaPP4qYqvDlrdoMwAI-RK-QbTLWllhKkrjxqmx47pZE7r0jnzr2jpqO1N5KkXCnqHCjXqizfo76rC0wl1y5MR1-1mlk80NdLYQBAErJzLVBqzoLfTNEwF7kHXK6GRIX_xOk)**

**Note:** I am only displaying 2/3 widgets which are requested. I could not figure out the 'apply algorithm' syntax in a timely manner.

**Public URL: [https://p.datadoghq.com/sb/2nwjq89stekm2l22-f25993fd79fa93cb18dcd7310fa86c5c](https://p.datadoghq.com/sb/2nwjq89stekm2l22-f25993fd79fa93cb18dcd7310fa86c5c)**

**Bonus Question: What is the Anomaly graph displaying?**

Didn't get this set up as per Note above.

##  ** Monitoring Data**

Set:
1.  Warning threshold of 500
2.  Alerting threshold of 800
3.  And also ensure that it will notify you if there is No Data for this query over the past 10m.

**![](https://lh5.googleusercontent.com/TwH54USP9BxWeTZvMnP53j1UXVSW78BLfgr-50_MJyFqIhaNZP5ug70IDdmMNL06vXsEcqUrcej_W5EtRqVu4lHX_tfqy_vt2qmGss8n2bC5Tr8U4SirrUgg5AWRqBqvmlR8BfcC)**

Send  an email whenever the monitor triggers & Create different messages based on whether the monitor is in an Alert, Warning, or No Data state:
**![](https://lh6.googleusercontent.com/XhWn8m-LN8wW-p38n5I0UkQIbSsNDotTOJK0ckKIH4IXxibvNrpV70NZHxklZpv38EHgnz7FnJQnR-9QvY4aswFzSs2kN_XSvd55gTKIe97JMz2SoUp0tYoiyKNq9RVOOJxgeITn)**

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state:

**![](https://lh5.googleusercontent.com/ct8uFMXO1JtK0NRDRUEMBhJDS4ubbHMlKOvyNhQv7EY6rv7ZMI5qZ_E9_nSpg7EQKLD0BAf5tJjQYgfj25DGdTIWBLB4taL_sZMDa4tSe29Bq5iMWuQ7Cy0RhdVQYUfsv0IlbW2o)**

When this monitor sends you an email notification, take a screenshot of the email that it sends you:
**![](https://lh6.googleusercontent.com/MaL4OAJNvvDSIP_MIj-q8kXHmZ2XckW7-8izhb3DnMo8nT-KQKMB8MjV2v0lf7YDdEL3HeJl_M5ICT82rJ0RAJGXF1n4fsCrgFCUYA3y20dHmqTOR3gt8KYlHUZYoUctAV_D1pm7)**

Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

-   One that silences it from 7pm to 9am daily on M-F:
- **![](https://lh5.googleusercontent.com/8xlFOr5ok6KYrMJudOpLCfR3VWGvQhXStnkTdvCTk5tf_rQV7CZKwE4p0QEOLdGCtwWxjFNW9uSN8dG5Y-GphkEABjf7f0nV5Sd799Oynm700GuFA-Haj3pZTHQ-V7Z8DQeHcp-D)**
-  And one that silences it all day on Sat-Sun:
- **![](https://lh5.googleusercontent.com/1a96snAjKeuGuS3c7ZNq8ZBqXWhmddjIPUGaYFfVJ3XvQcHQaOKNVtrXIqeRMeejO_1I9QV-Shyowrq8j9gbvpinsxa0efjL2Kxcx1gdnVUIyzKFM2jOltpkOCOcCJVzXW2bKkk0)**

Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification:
**![](https://lh3.googleusercontent.com/412YdE3ZFNPP6EiOe4si2hwdKNSngafY3xghvt9jh-4wbg94GKHTQyQt5hHPhSQmw06JMNq-lEsDDD85u3uTTC-YssLOBkLbzTxaywrsqUUWsnHFNrvh8IcD5Yaw_oJr2A5Wps9y)**

##  APM setup

Flask App v1:
**![](https://lh6.googleusercontent.com/7lio2z03ArcAja1tuuzT6zarann-a4YrQUPFXeb1ak85xDK_15HbNOf0fjM_z_ULN6sQNrYFLaBnbCL2xTvbua6A5FVGj0QPsFaDTvFtsNVSRCGWIjcdYN-9yaXuwltVedyBTwKq)**

V2:
**![](https://lh6.googleusercontent.com/_FDwsIyU56mcJvqT3NbEom94b53jbzNdUcXLJHyaay12srRwpAgGWo9gu3skR0I6O8Bssk-4lnzHfj37g50gp3Yq7UazDCbwbxM2KinveNEpMBfaHGV4HIO4kcrN4OzNB31XD9-r)**

APM instrumented:
**![](https://lh6.googleusercontent.com/mq6jUJtukjnzEd979PAbUym5oane3NDX23moZz2KkvlfyDly1KEOddpKMOZNTLLBbblw1ryr9_1-HyYyw3PAUoIf8rRJSxQVQuJeDCPFg5wqLKta2BT9Ve3N7XhPdfXsj6GEaFpY)**

**![](https://lh5.googleusercontent.com/aKW8TRnJKg9dFXGwCTRAgEJ-5YWk0j63pw44RlRyNWWH6B6-w4fHADIYn-mge5Utp_vfEc7hX9cU-ShmBoLrtfLjkt1-ZOQ0uls5DHJKXSSVPl8No9toXxC2e43CTQUAvu9fNaCD)**

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics:
**![](https://lh4.googleusercontent.com/dI9P2ULx0u7fE7XJy0cyCa0yCpXiiiI_o-i9RcuhLz9bvmw856-Dh1yW1hkhViwI2iOlb-PRdLl-xgh97zBKrC-HqV7ipTWd6im-zGBAwdjN6GDcBh-hSxB2BYNi3autQnqiK_Ip)**
**Public dash link: [https://p.datadoghq.com/sb/2nwjq89stekm2l22-f25993fd79fa93cb18dcd7310fa86c5c](https://p.datadoghq.com/sb/2nwjq89stekm2l22-f25993fd79fa93cb18dcd7310fa86c5c)**

**Please include your fully instrumented app in your submission, as well?**

I don’t know what this means…

I ‘installed’ the example Flask webapp given and instrumented it as above.

I'm happy to update this assignment in any way you guys seem fit.

## Final Question:

I have just recently begun investing in Cryptocurrencies but have been fascinated by the tech for a few years now.

I can see how Datadog monoriting and alerts could be set up not just to simply watch the price of, for example, Bitcoin - but to monitor for anomalies relating to important metrics like the 100 and 200 day moving average price.

Devations from these and other key metrics are important indicators for the market overall and this kind of data could allow you to better inform your investing strategy.

Really, there is an incredibly number of useful things you could do here.

Collecting APM Data
===================


1. Enable APM in the Agent Config file

\

    ``sudo vim /etc/datadog-agent/datadog.yaml``

\

    .. image:: images/enable_apm_config.png
        :align: center

\


2. Install ddtrace

\

    ``pip install ddtrace``

\

3. Install Flask

\

    ``pip install flask``

\

4. Create Python file that contains the Flask App provided

\
    ``vagrant@vagrant:~$ sudo vim /etc/python/flaskApp.py``

\

    .. image:: images/flaskapp.png
        :align: center

\

5. Start the Flask App with the following command:

\

    ``vagrant@vagrant:~$ DD_SERVICE="myFlaskApp" DD_ENV="dev" DD_LOGS_INJECTION=true ddtrace-run python /etc/python/flaskApp.py``

\
    .. image:: images/start_flask_app.png

\

6. Once we see ddtrace active, run the following curl command to test the endpoints

\
    ``curl 127.0.0.1:5050``

\
    ``curl 127.0.0.1:5050/api/apm``

\
    ``curl 127.0.0.1:5050/api/trace``

\
    ``curl 127.0.0.1:5050/test``

\

7. The requests were successfully traced. Each trace represents the time spent by the application processing request. All traces are OK.

\
    .. image:: images/apm1.png
        :align: center

\

    .. image:: images/apm2.png
        :align: center

\

    - By looking deeper into this trace, you can see each span that makes up the request.

\

    .. image:: images/apm3.png
        :align: center

\

    .. image:: images/apm4.png
        :align: center

\

    .. image:: images/apm5.png
        :align: center

\

8. APM Data Timeboard

\

    .. image:: images/apm6_dashboard.png
        :align: center

\

    `APM and Infrastructure Metrics Dashboard <https://p.datadoghq.com/sb/708a2847-9e46-11ec-854a-da7ad0900002-49cb9e37ff0ae5d760535ccd323c6ee2>`__

**Bonus**: Service vs Resource
    - Service - A service is a build block in computing architecture. It groups together enpoints, quereies, or jobs to build your application.
    - Resource - A resource represents a certain area of an application. It could be an instrumented web endpoint, database query,or background job.

\



Final Question
--------------

I think an ideal use for Datadog would be for the Bushnell Golf Speaker/Rangefinder. The product is great for an ideal day out on the course as it allows you to play music and also can tell you how far away the green is; even down to the detail of the front,center, and back of the green.
This app connects to your smartphone device and has majority of courses preloaded to the app.

Unfortunately, after a handful of uses my smartphone would not connect anymore to the device. With a lot of golfers on the course at once, bluetooth inteference can always be an issue. I ruled that out as I was the only device connected with bluetooth within 100 yards.
After reaching out to Bushnell's tech support they couldn't see anyting on their end to help troubleshoot and made it seem like my phone was the issue.

With Datadog monitoring, Bushnell would be able have visibilty to see the exact issue as to why the connection may be failing. To keep golfers satisfied, they would be able to reduce downtime and detect issues before they happen.
It would be easier to determine what the issue exactly is; whether it's at the device, application, or network level.






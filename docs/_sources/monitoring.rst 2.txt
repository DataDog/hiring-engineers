Monitoring Data
================

\

I created the monitors for ``my_metric`` through the Datadog UI

\


1. In the Datadog UI go to Monitors > New Monitor > select ``my_metric`` from the  "Define The Metric" category
\

    .. image:: images/my_metric_monitor_setup.png
        :align: center

\


2. Set the Alert Threshold of 800, the Warning Threshold of 500, and a notification email to be sent whenever data is msising for more than 10 minutes.
\

    .. image:: images/monitoringdata_warning_threshold.png
        :align: center

\

3. Set up email notifications depending on the Alert
\

   .. image:: images/alert_config.png
       :align: center


\

4. Email triggered and sent because of threshold
\

    .. image:: images/email_alert_new.png
        :align: center

\

**Bonus**:
\

1. Scheduled downtime alert from 7PM to 9AM daily on M-F

\

    .. image:: images/scheduled_downtime_m-f.png
        :align: center


\

2. Scheduled downtime alert every week for all day Saturday-Sunday

\

    .. image:: images/scheduled_down_weekends_alert.png
        :align: center


\







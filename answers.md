## What is the Agent?

The Datadog Agent is a piece of software installed on all of your hosts that will link them up to your Datadog infrastructure. Each Agent will send up data from their host providing you a map of all your data and metrics.

### Tags

Here is a screenshot of the host map with added tags.
![hosttags]

### Database Integration clone

This is a link to the timeboard clone of my database integration.
[Cloned Dash Link][dash]
Also a screenshot:
![dashboard]

## What is the difference between a timeboard and a screenboard?

When you create a dashboard you can choose between a TimeBoard or a ScreenBoard. Here is a brief overview of the two:

#### Timeboard

TimeBoards will appear as aligned rows and columns such that they simultaneously represent the same moment in time. This allows you to more clearly view correlations in your data and aid in troubleshooting.

#### ScreenBoard

ScreenBoards have a highly customizable display that you can hone to create the clearest and most relevant overview for your purposes. Whilst TimeBoards are always synced, you can use ScreenBoards to display data from many different ranges of time at once.

#### Which to use?

In summary, TimeBoards are preferable for troubleshooting and ScreenBoards are preferable for sharing information, especially more holistic data.

### Snapshot notification

Here is a screenshot of an @notification email showing test.support.random peaking over 0.9.
![snapshotpeak]

### Alert notification

Here is a screenshot of an alert email triggered when test.support.random peaks over 0.9 in a five minute window.
![peakingalert]

### Scheduled Downtime notification

Here is a screenshot of an email alerting a scheduled downtime on the alert above.
![downtime]





[hosttags]: ./images/host-with-tags.png
[snapshotpeak]: ./images/snapshot-peak.png
[peakingalert]: ./images/peaking-alert.png
[downtime]: ./images/downtime-notification.png
[dashboard]: ./images/dashboard.png
[dash]: https://app.datadoghq.com/dash/178726/postgres---overview-cloned

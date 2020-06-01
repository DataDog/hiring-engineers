## Bug Tracker

# 1. Typo found on downtime setup

![IMG 01](/images/bug-001-downtime-setup-typo.png)

# 2. Dashboard "Flask & System Infra Monitoring"

Issue seen where "Trace Flask Request Hits" widget is refreshing incorrectly.  Resolved by refreshing page in browser.  

`MacOS Firefox 76.0 (64-bit)`

`before page refresh:`

![IMG 02](/images/bug-002-widget-trace-flask-rqst-hits-updating-incorrectly.png)

`after page refresh:`


![IMG 03](/images/bug-002-widget-trace-flask-rqst-hits-refresh-fixes-it.png)

# 3. tv mode 

Tv mode does not work in firefox. In safari it does.

`MacOS Firefox 76.0 (64-bit)`

`MacOS Safari Version 13.1 (14609.1.20.111.8)`

# 4. container agent host disk util 

When deploying container agent the disk size was incorrectly measured. Appears to ~doubling actual disk size of 10GB.

![IMG 04](/images/bug-003-container_agent_disk_info_incorrect.png)



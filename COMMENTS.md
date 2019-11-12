## This is an overview of issues and observations while testing Datadog.

## Issue with Agent (Ubuntu)
### Symptom: 
Lot’s of error messages regarding reading disk when running status of Datadog Agent  - see below

`2019-10-30 05:56:27 CET | CORE | WARN | (pkg/collector/python/datadog_agent.go:116 in LogMessage) | disk:e5dffb8bef24336f | (disk.py:75) | Unable to get disk metrics for /var/lib/docker/overlay2/d8d0b290a8ed49ba0fd0fa560aeec53dc3d202e41fb130af8f07fa0e897909bf/merged: [Errno 13] Permission denied: '/var/lib/docker/overlay2/d8d0b290a8ed49ba0fd0fa560aeec53dc3d202e41fb130af8f07fa0e897909bf/merged’`

### Cause: 
Permission issue

### Solution: 

Was able to find identical error message in https://github.com/DataDog/dd-agent/issues/2932. Further examination pointed me to disk.yaml which is actually /etc/datadog-agent/conf.ddisk.d/conf.yaml.default in the current version. Put nsfs the blacklisted filesystems and the error disappeared.

## Google Cloud integration
When configuring Google Cloud following the documentation at https://docs.datadoghq.com/integrations/google_cloud_platform/?tab=datadogussite#setup, some of the roles that should be selected are no longer there (Cloud Asset - Cloud Asset Viewer, Monitoring - Monitoring Viewer).

The good news is that services are reported within Datadog.

## Datadog COM or EU
This bit me several times. The Datadog agent defaults to datadoghq.com, so my API key for datadoghq.eu is not going to work. Some of the documentation also points by default to .com (i.e. in the [Monitoring Flask](https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/#installing-the-datadog-agent "Monitoring Flask") manual assumes the .com site which for obvious resasons I am unable to login to with my EU account. Additionally the datadog.conf assumes the .com site. 

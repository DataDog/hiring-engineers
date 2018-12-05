import sys, json, base64, requests, urllib,time

from datadog import initialize, api

uri_base = 'https://api.datadoghq.com/api/'

options = {'api_key': 'b2a09e1d3eebae34b2fa02e37ee824e8',
           'app_key': 'b5df64de9f718407e456520074814c859c61404b'}

initialize(**options)

   
title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"},
    "title": "Average Memory Free"},
     {"definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:vagrant-ubuntu-trusty-64}"}],
        "viz": "timeseries"},
     "title": "mymetric"},
     {"definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:vagrant-ubuntu-trusty-64}.rollup(sum, 3600)"}],
        "viz": "query_value"},
     "title": "Rollup of mymetric - last hour"},
     {"definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.metrics.document.insertedps{host:DESKTOP-ID5D6FG}, 'basic', 3)"}],
        "viz": "timeseries"},
     "title": "Anomolies of Documents inserted per second"}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

try:
  msg = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
  print(msg)
  
except Exception as e:
   print(e)
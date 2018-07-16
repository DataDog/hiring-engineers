
# coding: utf-8

# In[1]:

from datadog import initialize, api

options = {
    'api_key': 'a32ed5c86d3cb70caac39a17d0800f1b',
    'app_key': '5bcb6a64e7c3f3ec1e78a007daeaddb9b0e9cad1'
}


# In[2]:

initialize(**options)

title = "My Timeboard-1"
description = "An informative timeboard."


# In[6]:

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:hello.my_metric{host:vagrant}",
                "type": "line",
                "style": {
                "palette": "dog_classic",
                "type": "solid",
                "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "avg"
            }
        ],
        "viz": "timeseries"
    },
    "title": "Average of My Metric"
}, {"definition": {
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "anomalies(avg:mongodb.connections.available{server:mongodb://_:_localhost:27017/admin}, 'robust', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ] },
  "title": "mongodb with anomalies"
}, {"definition": {
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "avg:hello.my_metric{host:vagrant}.rollup(sum, 60)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ]},
  "title": "ave of my_metric with rollup"
}]


api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs)


# In[ ]:




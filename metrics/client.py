import os
from collections import Iterable

import datadog


class GenericClient(object):
    def __init__(self, api_key=None, app_key=None):
        """
        Initializes the api client
        :param api_key: the data dog api ke
        :param app_key: the data dog app key/name
        :return: `None`
        """
        datadog.initialize()
        self.api = datadog.api
        key_name = 'DATADOG_API_KEY'
        if not api_key and not os.getenv(key_name):
            RuntimeError("Key not set in env or kwargs, please set {}".format(key_name))
        datadog.initialize(api_key, app_key)

    def create_event(self, title, text, tags, alert_type, priority, alert_handles=None):
        """
        Creates an event
        :param title: event title
        :param text: text of the event
        :param tags: tags associated with the event
        :param alert_type: type of alert
        :param priority: priority of the event
        :param alert_handle: any handles without the @ to notify
        :return:
        """
        if alert_handles:
            if isinstance(alert_handles, Iterable):
                handles = ' '.join(['@{}'.format(person) for person in alert_handles])
            else:
                handles = '@{}'.format(alert_handles)
            text = "{} -- {}".format(text, handles)
        return datadog.api.Event.create(title=title, text=text, tags=tags, alert_type=alert_type, priority=priority)

    def update_pageviews_and_latency(self, view_name, total_time, incr=1, extra_tags=None):
        """

        :param view_name:
        :param total_time:
        :param incr:
        :param extra_tags:
        :return:
        """
        tags = ['support', 'page:{}'.format(view_name)]
        if extra_tags:
            tags += extra_tags
        datadog.statsd.increment('web.page_views', value=incr, tags=tags)
        datadog.statsd.histogram('web.page_latency', total_time, tags=tags)

    def query(self, start, end, query, tags=None):
        return self.api.Metric.query(start=start, end=end, tags=tags, query=query)

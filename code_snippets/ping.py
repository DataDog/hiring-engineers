import os
import subprocess
import re

import time
import requests

from checks import AgentCheck
from hashlib import md5

class PingCheck(AgentCheck):

  def check(self, instance):
    if 'host' not in instance:
      self.log.info("Skipping instance, no host found.")
      return

    # Load values from the instance configuration
    host = instance['host']
    server_num = instance['server_num']


    # Use a hash of the host as an aggregation key
    aggregation_key = md5(host).hexdigest()

    # Check the host

    proc = subprocess.Popen(
      ['ping', '-c', '3', host],
      stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if stderr:
      self.event({
        'timestamp': int(time.time()),
        'event_type': 'icmp_check',
        'msg_title': 'error',
        'msg_text': stderr,
        'aggregation_key': aggregation_key
      })
    elif proc.returncode == 0:
      # Submit a gauge
      res = re.search('(?<=time=).*?(?=\sms)', stdout).group()
      self.gauge('icmp.riot_response_time.' + str(server_num), res, tags=['icmp_check'])
    elif proc.returncode == 1:
      # Make an event
      self.event({
        'timestamp': int(time.time()),
        'event_type': 'icmp_check',
        'msg_title': 'host_unresponsive',
        'msg_text': 'Server %s timed out.' % (server_num),
        'aggregation_key': aggregation_key
      })


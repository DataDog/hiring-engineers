# the following try/except block will make the custom check compatible with any Agent version
try:
            # first, try to import the base class from old versions of the Agent...
                        from checks import AgentCheck
except ImportError:
            # ...if the above failed, the check is running in Agent version 6 or later
                        from datadog_checks.checks import AgentCheck

                        # content of the special variable __version__ will be shown in the Agent status page
                        __version__ = "1.0.0"


import requests

class WeatherCheck(AgentCheck):
        def check(self, instance):
            url = 'https://api.darksky.net/forecast/78082a2307c27bc8308340cd3e2ffa5b/40.7128,-74.0060'
            resp = requests.get(url=url, params='')
            data = resp.json()
            self.gauge('temperature', data['currently']['temperature'])
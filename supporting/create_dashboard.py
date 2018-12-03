"""
This script is part of the SE test for Datadog.  It creates a dashboard.
"""

from datadog import api, initialize

DDOG_API_KEY = ''
DDOG_APP_KEY = ''

def main():
    """
    Main interface to this function
    """

    initialize(DDOG_API_KEY, DDOG_APP_KEY)
    graphs = [
        {
            "definition": {
                "events": [],
                "requests": [
                    {"q": "my_metric{host:setest.mikemclaughlin.org}"}
                ],
                "viz": "timeseries"
            },
            "title": "Custom Metric"
        },
        {
            "definition": {
                "events": [],
                "requests": [
                    {"q": "anomalies(avg:mysql.performance.queries{*}, 'basic', 2)"}
                ],
                "viz": "timeseries"
            },
            "title": "MySQL Queries (with Anomalies shown)"
        },
        {
            "definition": {
                "events": [],
                "requests": [
                    {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
                ],
                "viz": "timeseries"
            },
            "title": "Custom Metric Rollup (sum of last hour)"
        }
    ]
    api.Timeboard.create(title='Visualizing Data',
                         description='Question 2 Timeboard',
                         graphs=graphs,
                         template_variables=[],
                         read_only=False)

if __name__ == "__main__":
    main()

from datadog import initialize, api
import time

options = {
    'api_key': '6ecfd1d61dff04a0547d44561ac09911',
    'app_key': '83bf20f58f0fcc8b3d891b7817ba5d02eefde58f'
}

initialize(**options)

start_ts = 1536379200
end_ts = start_ts + (24 * 60 * 60)

recurrence = {
    'type': 'weeks',
    'period': 1,
    'week_days': ['Sat', 'Sun']
}

api.Downtime.create(
    scope='host:datadog-project',
    start=start_ts,
    end=end_ts,
    recurrence=recurrence,
    monitor_id=6245105,
    message="@zgroves19@gmail.com Hi team I scheduled downtime for the my_metric monitor for the weekends so it wouldn't harass you while you're doing awesome things!")

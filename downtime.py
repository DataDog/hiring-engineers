from datadog import initialize, api
import time
import datetime

options = {
    'api_key': '2acf23a25b2f5b5286e9cbfb83fb612d',
    'app_key': 'df7063887cd81f2e02eae387ab2a01193e130a94'
}

initialize(**options)

# Repeat for 3 hours (starting now) on every week day for 4 weeks.
start_date = datetime.datetime(2018, 5, 21, 20, 0, 0)
start_ts = int(time.mktime(start_date.timetuple()))
end_ts = start_ts + (14 * 60 * 60)

recurrence = {
    'type': 'weeks',
    'period': 1,
    'week_days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
}

# Schedule downtime
api.Downtime.create(scope='*', message='Scheduled Downtime @kipmango@gmail.com', monitor_id='4996201', start=start_ts, end=end_ts, recurrence=recurrence, timezone='EST')
1:
The agent is a process that listens for metrics and events from the consumer's code, be it metrics from checks or the dogstatsd.

2:
Page views:
https://app.datadoghq.com/metric/explorer?from_ts=1415977991235&to_ts=1415978942250&tile_size=m&exp_metric=web.page_views&exp_scope=&exp_agg=avg&exp_row_type=metric

Latency:
https://app.datadoghq.com/metric/explorer?from_ts=1416232591669&to_ts=1416232891669&tile_size=m&exp_metric=web.latency.avg&exp_scope=&exp_agg=avg&exp_row_type=metric

3:
Stacked latency:
https://app.datadoghq.com/dash/dash/32225?from_ts=1416232719000&to_ts=1416233073000&tile_size=m

4:
Page views and views by page:
https://app.datadoghq.com/dash/dash/32211?from_ts=1416232713309&to_ts=1416233137957&tile_size=m

{
  "viz": "timeseries",
  "requests": [
    {
      "q": "sum:web.page_views{page:home}"
    },
    {
      "q": "sum:web.page_views{page:id2}"
    },
    {
      "q": "sum:web.page_views{page:id4}"
    },
    {
      "q": "sum:web.page_views{page:id5}"
    },
    {
      "q": "sum:web.page_views{page:id6}"
    },
    {
      "q": "sum:web.page_views{page:id7}"
    },
    {
      "q": "sum:web.page_views{*}"
    }
  ],
  "events": []
}

5:
test.support.value:
https://app.datadoghq.com/dash/dash/32247?from_ts=1416232208845&to_ts=1416233222929&tile_size=m



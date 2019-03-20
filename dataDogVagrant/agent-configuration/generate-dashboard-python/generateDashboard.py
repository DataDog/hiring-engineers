from datadog import initialize, api

options = {
    'api_key': 'ad00c177c779cc3d503ee10c55c302dd',
    'app_key': 'dfd765459564830537d9cb5f0cce7ccd7b402cff'
}

initialize(**options)

title = 'Custom Dashboard'
widgets = [
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:custom_metric{host:ubuntu}'},
            {'q': "anomalies(avg:system.load{host:ubuntu}, 'basic', 2"},
            {'q': "avg:custom_metric{host:ubuntu}.rollup(sum, 3600)"}
        ],
        'title': 'ubuntu - custom_metric'
    }
}]
    # {
    # 'definition': {
    #     'type': 'timeseries',
    #     'requests': [
    #         {'q': "anomalies(avg:system.load{host:ubuntu}, 'basic', 2"}
    #     ],
    #     'title': 'ubuntu postgres - system.load'
    # }},
    # {
    # 'definition': {
    #     'type': 'timeseries',
    #     'requests': [
    #         {'q': 'avg:custom_metric{host:ubuntu}.rollup(sum, 3600)'}
    #     ],
    #     'title': 'custom rollup - custom_metric - past hour'
    # }}
layout_type = 'ordered'
description = 'Custom Dashboard for DataDog SE Exercise Showing custom_metric, postgres system load, custom_metric rollup.'
is_read_only = True
notify_list = ['russelviola@gmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
print("end script")

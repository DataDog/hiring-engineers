from datadog import initialize, api

options = {
    'api_key': 'KEY',
    'app_key': 'KEY'
}

initialize(**options)

title = 'MySQL Stats'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'mysql.performance.cpu_time{host:i-0fcaadedac4ac5b29}'}
        ],
        'title': 'Bin Log Disk Use'
    }
}]
layout_type = 'ordered'
description = 'MySQL DB Information via APIs'
is_read_only = True
notify_list = ['creativevikram@gmail.com']
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list
                                         )
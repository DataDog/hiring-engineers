from datadog import initialize, api

options = {
    'api_key': '487aa562e368c18fddaee1f9a02cd5d5',
    'app_key': '2708b11b6abeeb93d1c8c849b2c54997ba9e2fe7'
}

initialize(**options)

title = 'Visualize Data Exercise'

widgets= [
{
    "definition":{
        "type":"timeseries",
        "requests": [
            {
                "q":"avg:my_metric{*}"
            }
        ],
        "title":"Average of my_metric"
    }
},
{
    "definition":{
        "type":"timeseries",
        "requests":[
            {

                "q":"anomalies(mongodb.atlas.system.cpu.mongoprocess.norm.kernel,'basic',2)"
            }
        ],
        "title":"Anomalies Function"
    }
},
{
    "definition":{
        "type":"timeseries",
        "requests":[
            {
                "q":"avg:my_metric{*}.rollup(sum,3600)"
            }
        ],
        "title":"Metric Rollup"
    }
}]


layout_type = 'ordered'
description = 'A dashboard using the DataDog API'
is_read_only = False
notify_list = ['shawnppitts@gmail.com']


api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list)
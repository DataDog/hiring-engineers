from datadog import initialize, api

options = {'api_key': '4e2177053a094d261c10e610b8ca8cdd',
            'app_key': '223159fe496e0c2506af146fa8f0eae896818531'
           }

initialize(**options)

title = "Visualizing Data using Dashboard:"
widgets = [{
            "definition": {
                            "type": "timeseries",
                            "requests": [
                                        {"q": "avg:Up_Down.my_metric{*}"}
                                        ],
                            "title": "Custom_Check"
                             },
            },
            {"definition": {
                            "type": "timeseries",
                            "requests": [
                                        {"q": "anomalies(max:mongodb.asserts.userps{*}, 'basic', 5)"}
                                        ],
                            "title": "No of asserts per sec (anomaly detection on)"
                             },
            },
            {"definition": {
                            "type": "distribution",
                            "requests": [
                                        {"q": "avg:Up_Down.my_metric{*}.rollup(sum, 3600)"}
                                        ],
                            "title": "Custom_Check with Rollup"
                            }
            }]

layout_type = "ordered"
description = "3 Widgets."
is_read_only = True
notify_list = ["kjo@itadel.dk"]
template_variables= None

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description, notify_list=notify_list,
                     template_variables=template_variables)

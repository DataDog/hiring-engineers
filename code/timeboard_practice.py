from datadog import initialize, api

options = {
    'api_key': '1589e4066ca4bc3cab3a8676b1e55a89'
,
    'app_key': '55cd01bdafc7e69dadf3f275b25113b41e834899'
}

initialize(**options)
body ={"title":"Delaney's Dashboard","description":"","widgets":[{"id":8976768557290444,"definition":{"title":"","title_size":"16","title_align":"left","show_legend":true,"legend_layout":"auto","legend_columns":["avg","min","max","value","sum"],"time":{},"type":"timeseries","requests":[{"queries":[{"data_source":"metrics","name":"query1","query":"avg:system.cpu.user{*}"}],"response_format":"timeseries","style":{"palette":"dog_classic","line_type":"solid","line_width":"normal"},"display_type":"line"}],"yaxis":{"scale":"linear","include_zero":true,"label":"","min":"auto","max":"auto"},"markers":[]}}],"template_variables":[],"layout_type":"ordered","is_read_only":false,"notify_list":[],"reflow_type":"auto","id":"tgx-try-vyn"}
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_views)   
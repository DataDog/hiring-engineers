{{#is_alert}} 
ALERT: my_metric has averaged more than 800 for the last 5 minutes! 
Host IP {{host.ip}} has reported an average value of  {{value}} during that time. Please take corrective action!
{{/is_alert}}


{{#is_warning}} Warning: Host IP {{host.ip}} reports that my_metric has averaged more than 500 for the last 5 minutes! {{/is_warning}}


{{#is_no_data}} 
Warning! No data has been reported by my_metric on Host IP {{host.ip}} in the last 10 minutes!
{{/is_no_data}}

Notify: @bradleyjshields@gmail.com 
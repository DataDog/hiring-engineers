#
# Cookbook:: chef_datadog_example
# Recipe:: dd_custom_check
#
# Copyright:: 2018, The Authors, All Rights Reserved.
template '/etc/datadog-agent/conf.d/my_metric.yaml' do
  source 'my_metric.yaml.erb'
  notifies :run, 'execute[restart-datadog-agent]'
end
  
template '/etc/datadog-agent/checks.d/my_metric.py' do
  source 'my_metric.py.erb'
  notifies :run, 'execute[restart-datadog-agent]'
end
#
# Cookbook:: chef_datadog_example
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.
include_recipe 'datadog::dd-agent'
include_recipe 'datadog::dd-handler'
include_recipe 'chef_datadog_example::mongodb'
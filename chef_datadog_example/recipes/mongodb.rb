#
# Cookbook:: chef_datadog_example
# Recipe:: mongodb
#
# Copyright:: 2018, The Authors, All Rights Reserved.



#
# Install mongodb
#
package 'mongodb'

#
# Start mongodb
#
service 'mongodb' do 
  action [:enable, :start]
end

#
# Setup the DataDog user in Mongo if not created
# 
execute 'setup-datadog-user' do 
  command <<-EOH 
    sleep 10
    mongo admin --eval "db.createUser({'user':'datadog', 'pwd': 'datadog', 'roles' : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})"
  EOH
  not_if 'mongo admin --eval \'db.getUsers()\'|tr -d \'\n\'|grep datadog'
end

#
# Command to restart the datadog-agent
#
execute 'restart-datadog-agent' do
  command 'service datadog-agent restart'
  action :nothing
end

template '/etc/datadog-agent/conf.d/mongo.yaml' do
  source 'mongo.yaml.erb'
  owner 'dd-agent'
  group 'root'
  mode '0600'
  notifies :run, 'execute[restart-datadog-agent]', :immediately
end

  
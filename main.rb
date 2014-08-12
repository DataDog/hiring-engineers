require 'dogapi'
require 'pry'

dog = Dogapi::Client.new(ENV["DATADOG_API_KEY"])

dog.emit_event(Dogapi::Event.new('cool this works', :msg_title => 'Test2'))


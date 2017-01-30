require 'dogapi'
require 'pry'

dog = Dogapi::Client.new(ENV["DATADOG_API_KEY"])

dog.emit_event(Dogapi::Event.new('@jbmilgrom@gmail.com - nice! this works', :msg_title => 'Test3'))


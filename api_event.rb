
require 'rubygems'
require 'dogapi'

api_key='30bb1d28fce2e3e1c2976895ec020abd'
app_key='91a4188beee745a5ff48aa35d3937f9c98e2baa9'

event = Dogapi::Client.new(api_key, app_key)

event.emit_event(Dogapi::Event.new('@matthewwmain@gmail.com Hello Datadog.', :msg_title => 'Hello'))
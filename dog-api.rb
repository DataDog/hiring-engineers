# authentication

require 'rubygems'
require 'dogapi'
require 'pry'

api_key = "dd855f1dee243106686bef188eb4de07"
app_key = "72b9e07910a733334c1400214fb8f12794ccd04b"


dog = Dogapi::Client.new(api_key, app_key)

response = dog.emit_event(Dogapi::Event.new('Datadog Event submission via API - @mstines007@gmail.com', :msg_title => 'Level 1 Email test'))


binding.pry


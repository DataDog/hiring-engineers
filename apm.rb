require 'sinatra'
require 'ddtrace'
require 'ddtrace/contrib/sinatra/tracer'
require 'logger'
require 'pry'

set :bind, '0.0.0.0'
set :port, 5050

logger = Logger.new(STDOUT)
logger.level = Logger::DEBUG
logger.progname = 'sinatra_app'
logger.formatter = proc do |severity, datetime, progname, msg|
    "[#{datetime}][#{progname}][#{severity}]#{msg}\n"
  end

Datadog.configure do |c|
    c.use :sinatra
end

Datadog.tracer.trace('sinatra.start') { logger.debug("Application start") }

get '/' do
    # Datadog.tracer.trace('get.root') { logger.debug("Get the root") }
    'Entrypoint to the Application'
end

get '/api/apm' do
    'Getting APM Started'
end

get '/api/trace' do
    'Posting Traces'
end
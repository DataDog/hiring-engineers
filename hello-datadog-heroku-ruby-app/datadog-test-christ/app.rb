require 'logger'
require "sinatra"
require 'datadog/statsd'
require 'ddtrace'
require 'ddtrace/contrib/sinatra/tracer'

logger = Logger.new(STDOUT)
logger = Logger.new(STDERR)

logger.info("Starting Stastd server")
statsd = Datadog::Statsd.new('localhost', 8125)


Datadog.configure do |c|
  c.use :sinatra, service_name: 'hello-datadog-heroku-ruby'
end

get "/" do
  logger.info("Index Page hit")
  statsd.increment('page.views', tags: ['page:index'])

  render :html, :index
end

get "/new-page" do
  logger.info("New Page hit")
  statsd.increment('page.views', tags: ['page:new-page'])

  render :html, :index
end

get "/error" do
  logger.error("Error Page hit")
  statsd.increment('page.views', tags: ['page:error-page'])

  raise "error"
end

error do
  "Error"
end

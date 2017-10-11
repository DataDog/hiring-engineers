# Import the library
require 'datadog/statsd'

# Create a statsd client instance.
statsd = Datadog::Statsd.new

# Load the dogstats module.
# require 'statsd'

# # Create a stats instance.
# statsd = Statsd.new('localhost', 8125)

# Increment a counter.
statsd.increment('rubyapp.pages.views')

statsd.gauge('users.online', 123, :sample_rate=>0.5)

# Sample a histogram
statsd.histogram('file.upload.size', 1234)

# Time a block of code
# statsd.time('page.render') do
#   render_page('home.html')
# end

# Send several metrics at the same time
# All metrics will be buffered and sent in one packet when the block completes
statsd.batch do |s|
  s.increment('page.views')
  s.gauge('users.online', 123)
end

# Tag a metric.
statsd.histogram('query.time', 10, :tags => ["version:1"])

# Post a simple message
statsd.event("There might be a storm tomorrow", "A friend warned me earlier.")

# Cry for help
statsd.event("SO MUCH SNOW", "Started yesterday and it won't stop !!", :alert_type => "error", :tags => ["urgent", "endoftheworld"])
from web import application
import datadog_setup
from datadog.dogstatsd import statsd

# Define a simple web application.
urls = (
    "^/?$", "Home",
    "^/about/?$", "About",
    "^/contact/?$", "Contact",
)
app = application(urls, globals())

class Home:
    @statsd.timed("page.latency")
    def GET(self):
        # Increment the page view counter every time the home page is viewed.
        statsd.increment("page.views")
        return "Home"

class About:
    def GET(self):
        return "About"

class Contact:
    def GET(self):
        return "Contact"

if __name__ == "__main__":
    app.run()
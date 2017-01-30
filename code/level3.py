# Enhanced version of Level 2.
from random import randint
from time import sleep
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
    @statsd.timed("page.latency", tags=["support", "page:home"])
    def GET(self):
        # Increment the page view counter every time the home page is viewed.
        statsd.increment("page.views", tags=["support", "page:home"])
        # Add random delay.
        sleep(randint(0, 2))
        return "Home"


class About:
    @statsd.timed("page.latency", tags=["support", "page:about"])
    def GET(self):
        # Increment the page view counter every time the about page is viewed.
        statsd.increment("page.views", tags=["support", "page:about"])
        # Add random delay.
        sleep(randint(0, 2))
        return "About"


class Contact:
    @statsd.timed("page.latency", tags=["support", "page:contact"])
    def GET(self):
        # Increment the page view counter time the contact page is viewed.
        statsd.increment("page.views", tags=["support", "page:contact"])
        # Add random delay.
        sleep(randint(0, 2))
        return "Contact"

if __name__ == "__main__":
    app.run()
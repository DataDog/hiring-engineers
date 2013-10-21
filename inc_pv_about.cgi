#!/usr/bin/python
# Required header that tells the browser how to render the text.
print("Content-Type: text/plain\n\n")  # here text -- not html
# Print a simple message to the display window.
#print("Hello, World!\n")

from statsd import statsd
from dogapi import dog_http_api as api
api.api_key = 'a87f80079d0fccc4eded3f079f7b605e'
api.application_key = '576ef5c9e5d44b6e2f01e06420111666ec5a1007'
statsd.increment('about.page_v', 10, tags=['about:about.html'])
print("It worked!")


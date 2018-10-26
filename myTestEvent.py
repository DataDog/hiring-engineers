from datadog import initialize, api

options = {
    'api_key': '9fcece82deb81b6846ad9d9b85893fda',
    'app_key': 'f06fdf0ac3ab382b8e33ecc2d4462b6588a00bca'
}

initialize(**options)
title = "Something big happened!"
text = 'And let me tell you all about it here!'
tags = ['version:1', 'application:web']

api.Event.create(title=title, text=text, tags=tags)

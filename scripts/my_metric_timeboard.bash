!#/bin/bash

api_key=xyz
app_key=13969b2a81854ff84b1705865086b4418830f0fb

curl -X POST -H "Content-type: application/json" \
-d '{
        "width": 1024,
        "height": 768,
        "board_title": "dogapi my_metric",
        "widgets": [
            {
              "type": "image",
              "height": 20,
              "width": 32,
              "y": 7,
              "x": 32,
              "url": "https://thumbs.dreamstime.com/b/teacher-programming-icon-isolated-white-background-teacher-programming-icon-119030737.jpg"
            }
        ]
}' \
"https://api.datadoghq.eu/api/v1/screen?api_key=${api_key}&application_key=${app_key}"

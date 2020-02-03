"""
This is a dummy service that our main Flask app calls when it on its /api/trace endpoint.
This service "fails" about 1 in 50 times. When it does, it takes significantly longer to send a response.
"""

import random
import time

from flask import Flask, Response

app = Flask(__name__)


@app.route('/api/resource')
def get_resource():
    will_resource_fail = random.randint(0, 50) == 25
    ms_to_wait = random.randint(0, 100) if not will_resource_fail else random.randint(500, 1000)

    time.sleep(ms_to_wait / 1000)

    return Response(
        response=None,
        status=500 if will_resource_fail else 200,
        content_type='application/json'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5051')

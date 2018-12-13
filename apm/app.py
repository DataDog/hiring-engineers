from ddtrace import patch_all
patch_all()

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run()

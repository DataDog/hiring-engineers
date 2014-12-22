from flask import Flask
from dogapi import dog_stats_api as dd
import os

dd.start(api_key =os.environ['DOGAPIKEY'])
app =  Flask(__name__)

@dd.timed('hello_World.duration')
@app.route("/")
def hello_World():
    return  "Hello World"

@app.route('/post/<int:post_id>')
@dd.timed('post.duration')
def post_it(post_id):
    return 'Post %s' %post_id

if __name__ == "__main__":
    app.run()

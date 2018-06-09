from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return 'Woohoo'

if __name__ == '__main__':
  app.run(debug=True)

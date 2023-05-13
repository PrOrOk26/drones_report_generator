# Add this to app.py
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hw')
def hello_world2():
    return 'Hello World 222!'


if __name__ == "__main__":
    app.run()

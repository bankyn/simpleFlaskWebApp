from flask import Flask
from functions import search4letters

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/search4')
def do_search() -> str:
    return str(search4letters('life, the universe, and everything!', 'eiru,!'))

if __name__ == '__main__':
    app.run()

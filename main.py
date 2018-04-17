from flask import Flask, render_template
from functions import search4letters

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/search4')
def do_search() -> str:
    return str(search4letters('life, the universe, and everything!', 'eiru,!'))

@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to the web search for letters app!')

if __name__ == '__main__':
    app.run()

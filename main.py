from flask import Flask, render_template, request
from functions import search4letters

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/search4', methods=['POST', 'GET'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    title = 'Here are your search matches:'

    return render_template('results.html', the_title=title, the_results=results, the_letters=letters, the_phrase=phrase)


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to the web search for letters app!')


if __name__ == '__main__':
    app.run()

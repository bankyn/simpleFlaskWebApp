from flask import Flask, render_template, request, redirect
from functions import search4letters

app = Flask(__name__)

def log_request(req: 'flask_request', res: str) -> None:
    with open('lsearch.log', 'a') as log:
        print(req, res, file=log)


@app.route('/search4', methods=['POST', 'GET'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    tmp_results = search4letters(phrase, letters)

    if tmp_results:
        results = ''.join(i + ',' for i in tmp_results).rstrip(',')
    else:
        results = '(no match)'
    title = 'Letter Search Results'
    log_request(request, results)

    return render_template('results.html', the_title=title, the_results=results, the_letters=letters, the_phrase=phrase)


@app.route('/')
@app.route('/entry', methods=['POST', 'GET'])
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to the search for letters app!')

if __name__ == '__main__':
    app.run(debug=True)  # flask defaults: (host='127.0.0.1', port=5000)
    # app.run(host='0.0.0.0', port=80)

from flask import Flask, render_template, request, redirect, escape
from functions import search4letters
from functions import UseDatabase

app = Flask(__name__)

table_name = 'vsearchlog'
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpassword',
                          'database': 'vsearchlogDB', }


def log_request(req: 'flask_request', res: str) -> None:
    """Log details of the web request and the results"""
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into {}
                  (phrase, letters, results, ip, browser_string)
                  VALUES 
                  (%s, %s, %s, %s, %s)""".format(table_name)
        cursor.execute(_SQL, (req.form['phrase'],
                               req.form['letters'],
                               res,
                               req.remote_addr,
                               req.user_agent.browser, ))


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


@app.route('/viewlog', methods=['POST'])
def view_the_log() -> 'html':

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = 'select phrase, letters, results, ip, browser_string from {}'.format(table_name)
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    page_title = 'View Log'
    titles = ('Phrase', 'Letters', 'Results', 'Remote_addr', 'User_agent')
    return render_template('viewlog.html', the_title='View Log', the_data=contents, the_titles=titles)


@app.route('/clearlog', methods=['POST'])
def clear_the_log():
    open('lsearch.log', 'w').close()
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run(debug=True)  # flask defaults: (host='127.0.0.1', port=5000)
    # app.run(host='0.0.0.0', port=80)
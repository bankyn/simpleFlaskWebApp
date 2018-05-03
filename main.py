from flask import Flask, render_template, request, redirect, escape
from functions import search4letters

app = Flask(__name__)

def log_request(req: 'flask_request', res: str) -> None:
    with open('lsearch.log', 'a') as log:
        print(req.form, res, req.remote_addr, req.user_agent, file=log, sep='|')

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
def view_the_log() -> str:
    contents = []
    with open('lsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    page_title = 'View Log'
    titles = ('Form Data', 'Results', 'Remote Addr', 'User_agent')
    return render_template('viewlog.html', the_title=page_title, the_data=contents, the_titles=titles)
    #return str(contents)

@app.route('/clearlog', methods=['POST'])
def clear_the_log():
    open('lsearch.log', 'w').close()
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)  # flask defaults: (host='127.0.0.1', port=5000)
    # app.run(host='0.0.0.0', port=80)
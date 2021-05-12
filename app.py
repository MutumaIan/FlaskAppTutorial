from flask import Flask, render_template, request, redirect, url_for, flash , abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'fsagsg9sg6s96hs96h9s6h'

@app.route('/') #specifies that someone has visited the base url page
def home():
    return render_template('home.html', codes=session.keys())

#Here the user will submit the form and generate the short code
@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That shortname has already been taken, please select another name')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'urls':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/mnt/e/Study/flask_tutorial/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}

        

#create a json file and dump the url and short code.
        with open('urls.json', 'w') as urls_file:
            json.dump(urls, urls_file)
            session[request.form['code']]  = True

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)

#For error handlings
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


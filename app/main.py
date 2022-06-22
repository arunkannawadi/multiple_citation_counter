from flask import Flask, Response, render_template, request
from . import backend
import time
import re

app = Flask(__name__)

@app.route("/timer")
def home_view():
    def inner():
        for x in range(100):
            time.sleep(1)
            yield '%s<br/>\n' % x
    return Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show the partial page immediately

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        return 'A GET request was made'
    elif request.method != 'POST':
        return 'Not a valid request method for this route'

    url=request.form['url']
    matches = re.findall("user=[^&]*", url)
    if matches is None or len(matches)==0:
        return 'No user specified'
    elif len(matches)>1:
        return 'Multiple users specified'
    scholar_id = matches[0][5:]

    scraper_api_key = request.form['shortcode'] if request.form['shortcode'] else None
    if scraper_api_key is not None and len(scraper_api_key) != 32:
        return 'Invalid scraper API key'

    max_paper_count = request.form['max_paper_count'] if request.form['max_paper_count'] != "" else None
    if max_paper_count is not None and max_paper_count.isdigit() is False:
        return 'Enter an natural number of papers to look for, or leave it empty'
    else:
        max_paper_count = int(max_paper_count)

    return Response(backend.main(scholar_id, scraper_api_key=scraper_api_key, max_paper_count=max_paper_count), mimetype='text/html')

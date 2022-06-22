from flask import Flask, Response, render_template
import time
 
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

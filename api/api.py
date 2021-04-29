import json
from flask import Flask, request, render_template
from config import Config
from forms import submitJobForm
import jobs

app = Flask(__name__)

# getting secret key from env var
app.config.from_object(Config)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/insert')
def insert():
    form = submitJobForm()
    return render_template('insert.html', form=form)

@app.route('/jobs', methods=['POST'])
def add_job():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job))

@app.route('/get_jobs', methods=['GET'])
def get_jobs():
    return json.dumps(jobs.get_jobs())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

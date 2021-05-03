import json
from flask import Flask, request, render_template
from config import Config
from forms import submitInsertForm, submitQueryForm, submitDeleteForm, submitUpdateForm
import jobs

app = Flask(__name__)

# getting secret key from env var
app.config.from_object(Config)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/insert')
def insert():
    form = submitInsertForm()
    return render_template('insert.html', form=form)

@app.route('/update')
def update():
    form = submitUpdateForm()
    return render_template('update.html', form=form)

@app.route('/query')
def query():
    form = submitQueryForm()
    return render_template('query.html', form=form)

@app.route('/delete')
def delete():
    form = submitDeleteForm()
    return render_template('delete.html', form=form)

@app.route('/getJobs', methods=['GET'])
def jobs_page():
    return render_template('jobs.html')

@app.route('/database', methods=['GET'])
def entries():
    return render_template('entries.html')


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

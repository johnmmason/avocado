import json
from flask import Flask, request, render_template, send_file, abort
from config import Config
from forms import submitInsertForm, submitQueryForm, submitDeleteForm, submitUpdateForm
import jobs
import time

app = Flask(__name__)

# getting secret key from env var
app.config.from_object(Config)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/formSubmit')
def insert():
    return render_template('formSubmit.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/getJobs', methods=['GET'])
def jobs_page():
    jobsData = json.loads(get_jobs())
    return render_template('jobs.html', data=jobsData)

@app.route('/jobs', methods=['POST'])
def add_job():
    try:
        job = json.loads(request.form.get('jsonData'))
    except Exception as e:
        return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    jobData = jobs.add_job(job)

    while(jobData['status']=='submitted'):
      jobData = jobs.get_job(jobData['job_id'])
      time.sleep(2)
    jobData = json.dumps(jobs.get_job(jobData['job_id']))
    jsonData = json.loads(jobData)
    
    # render a different form for a plot
    if (jsonData['job_type'] == 'plot'):
      job_link = "https://isp-proxy.tacc.utexas.edu/phart/download/" + jsonData['job_id']
      return render_template('plot.html', job_id = jsonData['job_id'], job_link = job_link)
    
    return render_template('formReturn.html', job_type = jsonData['job_type'], data = jobData)

@app.route('/raw_jobs', methods=['POST'])
def raw_job():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job))

@app.route('/get_jobs', methods=['GET'])
def get_jobs():
    return json.dumps(jobs.get_jobs())

@app.route('/get_job', methods=['POST'])
def get_job_form():
    job_dict = jobs.get_jobs()
    jid = request.form.get('jsonData')
    try:
        strJob = json.dumps(job_dict[ jobs._generate_job_key(jid) ])
        jsonData = json.loads(strJob)
        return render_template('jobReturn.html',jsonData = jsonData, data = strJob)
    except:
        return abort(404)

@app.route('/get_job/<jid>', methods=['GET'])
def get_job(jid):
    job_dict = jobs.get_jobs()
    try:
        return json.dumps( job_dict[ jobs._generate_job_key(jid) ], indent=4 )
    except:
        return abort(404)

@app.route('/download/<jid>', methods=['GET'])
def download(jid):
    try:
        IMG_PATH = jobs.get_plot(jid)
        return send_file(IMG_PATH, mimetype='image/png')
    except:
        return abort(404)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

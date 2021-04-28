import json
from flask import Flask, request
import jobs

app = Flask(__name__)

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

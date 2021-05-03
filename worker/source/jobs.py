import uuid
from hotqueue import HotQueue
import redis
import os
import datetime
import json

# fill in with the IP of the redis service later
q = HotQueue("queue", host=os.environ['REDIS_HOST'], port=6379, db=1)
rd = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    return 'job.{}'.format(jid)

def _instantiate_job(jid, start, end, data):
    job_dict = {}
    if type(jid) == str:
        job_dict['id'] = jid
        job_dict['start'] = start
        job_dict['end'] = end
    else:
        job_dict['id'] = jid.decode('utf-8')
        job_dict['start'] = start.decode('utf-8')
        job_dict['end'] = end.decode('utf-8')

    job_dict['job_specs'] = data

    return job_dict

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.set(job_key, (json.dumps(job_dict)).encode('utf-8'))

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(data):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    # attach job id to data
    data['id'] = jid
    data['submitted'] = str(datetime.datetime.now())
    _save_job(_generate_job_key(jid), data)
    _queue_job(jid)
    return data

def get_job(jid):
    jid = _generate_job_key(jid)
    job = json.loads( rd.get(jid).decode('utf-8') )
    return job

def update_job(job, params): # startFin is a string either 'start' or 'end'
    """Update the status of job with job id `jid` to status `status`."""
    for key in params.keys():
        job[key] = params[key]

    _save_job( _generate_job_key(job['id']), job )

# return all jobs in the redis database
def get_jobs():
    db_data = {}
    # iterate through all the keys in the redis db
    for key in rd.keys():
      db_data[key.decode('utf-8')] = rd.hgetall(key)

    return db_data

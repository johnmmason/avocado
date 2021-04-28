import uuid
from hotqueue import HotQueue
import redis
import os
import datetime

# fill in with the IP of the redis service later
q = HotQueue("queue", host='redis', port=6379, db=1)
rd = redis.StrictRedis(host='redis', port=6379, db=0)

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

    job_dict['data'] = data

    return job_dict

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    # attach job id to job dict
    job_dict = _instantiate_job(jid, "", "", {})
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict

def update_job(jid, startFin, data): # startFin is a string either 'start' or 'end'
    """Update the status of job with job id `jid` to status `status`."""
    jid, start, end, data  = rd.hmget(_generate_job_key(jid), 'id', 'start', 'end', 'data')
    job = _instantiate_job(jid, start, end, data)
    if job:
        # update start or end timestamp
        job[startFin] = datetime.datetime.now()
	# append data key from function param
        job['data'] = data
        _save_job(_generate_job_key(job['id']), job)
    else:
        raise Exception()

# return all jobs in the redis database
def get_jobs():
    db_data = {}
    # iterate through all the keys in the redis db
    for key in rd.keys():
      db_data[key.decode('utf-8')] = rd.hgetall(key)

    return db_data  

import uuid
from hotqueue import HotQueue
import redis
import os
import datetime
import json

# fill in with the IP of the redis service later
q = HotQueue("queue", host='redis', port=6379, db=11)
rd = redis.StrictRedis(host='redis', port=6379, db=10)

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

def update_job(jid, startFin, data): # startFin is a string either 'start' or 'end'
    """Update the status of job with job id `jid` to status `status`."""
    # update start or end timestamp
    data[startFin] = str(datetime.datetime.now())
    _save_job(_generate_job_key(jid), data)

def _decode_dict(data):
    decoded_data = {}

    for key in data.keys():
        if isinstance(key, bytes):
            decoded_data[key] = data[key].decode('utf-8')        
        if isinstance(data[key], dict):
            decoded_data[key] =  _decode_dict(data[key])
        elif isinstance(data[key], list):
            decoded_list = []
            for item in data[key]:
                decoded_list.append( _decoded_dict(item) )
            decoded_data[key] = decoded_list
        else:
            raise Exception

    return decoded_data

# return all jobs in the redis database
def get_jobs():
    db_data = {}
    # iterate through all the keys in the redis db
    for key in rd.keys():
      db_data[key.decode('utf-8')] = json.loads( rd.get(key).decode('utf-8') )

    return db_data  

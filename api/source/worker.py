from jobs import get_job, update_job
import database, json
from hotqueue import HotQueue
from psycopg2 import OperationalError

q = HotQueue("queue", host='10.110.128.5', port=6379, db=1)

@q.worker
def run_job(jid):
    job = get_job(jid)
    job_type = job['job_type']

    print("Accepted job " + job['id'] + ".")
    
    if job_type == "insert":
        
        try:
            database.insert(job['data'])
            update_job(job, {"status": "success"})
        except OperationalError:
            update_job(job, {"status": "failed", "error": "unable to connect to database"})
        except Exception as error:
            update_job(job, {"status": "failed", "error": str(error)})

    elif job_type == "query":
        try:
            data = database.get(job['cols'], job['params'])
            update_job(job, {"status": "success", "data": data })
        except Exception as error:
            update_job(job, {"status": "failed", "error": str(error)})

    elif job_type == "update":
        try:
            database.update(job['data'], job['params'])
            update_job(job, {"status": "success"})
        except Exception as error:
            update_job(job, {"status": "failed", "error": str(error)})

    elif job_type == "delete":
        try:
            database.delete(job['params'])
            update_job(job, {"status": "success"})
        except Exception as error:
            update_job(job, {"status": "failed", "error": str(error)})

    else:
        update_job(job, {"status": "failed", "error": "unknown job type"})

run_job()

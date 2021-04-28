import database, json
from psycopg2 import OperationalError

def __update_job(job, params):
    for key in params.keys():
        job[key] = params[key]
    return job

def run_job(job):
    job_type = job['job_type']
    
    if job_type == "insert":
        
        try:
            database.insert(job['data'])
            job = __update_job(job, {"status": "success"})
        except OperationalError:
            job = __update_job(job, {"status": "failed", "error": "unable to connect to database"})
        except Exception as error:
            job = __update_job(job, {"status": "failed", "error": str(error)})
            
        return job

    elif job_type == "query":
        try:
            data = database.get(job['cols'], job['params'])
            job = __update_job(job, {"status": "success", "data": data })
        except Exception as error:
            job = __update_job(job, {"status": "failed", "error": str(error)})

        return job

    elif job_type == "update":
        try:
            database.update(job['data'], job['params'])
            job = __update_job(job, {"status": "success"})
        except Exception as error:
            job = __update_job(job, {"status": "failed", "error": str(error)})

        return job

    elif job_type == "delete":
        database.delete(job['params'])
        job = __update_job(job, {"status": "success"})

        return job

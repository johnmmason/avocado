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

    if job_type == "query":
        #try:
        data = database.get(job['cols'], job['params'])
        job = __update_job(job, {"status": "success", "data": data })
        #except Exception as error:
        #    job = __update_job(job, {"status": "failed", "error": str(error)})

        return job
    
if __name__ == '__main__':    

    data = {
        "week_id": 1,
        "week": "01/01/12",
        "price": 1.243,
        "volume": 2,
        "total_4046": 700,
        "total_4225": 800,
        "total_4770": 900,
        "category": "conventional",
        "year": 2012,
        "region": "Atlanta"
    }

    job = {
        "job_type": "insert",
        "status": "submitted",
        "data": data
    }

    print(json.dumps(run_job(job), indent=4))
    
    job = {
        "job_type": "query",
        "status": "submitted",
        "cols": ['id', 'price'],
        "params": [{
            "column": "year",
            "type": "equals",
            "value": 2012
            },
            {
            "column": "volume",
            "type": "equals",
            "value": 2
            }]
    }
    print (json.dumps(run_job(job), indent=4))
        

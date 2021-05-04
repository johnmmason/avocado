import database, json
from psycopg2 import OperationalError
from jobs import q, get_job, update_job, save_plot
import analytics

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

    elif job_type == "plot":

        PLOT_TYPES = ['bar', 'line', 'box']
        try:
            assert job['plot_type'] in PLOT_TYPES, 'Invalid plot type'
        except Exception as error:
            update_job(job, {"status": "failed", "error": str(error)})
            return
            
        if job['plot_type'] == "box":
            try:
                plt = analytics.box_plot(job['columns'], job['params'])
                save_plot(jid, plt)
                update_job(job, {"status": "success", "img_id": jid})
            except Exception as error:
                update_job(job, {"status": "failed", "error": str(error)})
        else:
            update_job(job, {"status": "failed", "error": "plot_type not implemented"})

    else:
        update_job(job, {"status": "failed", "error": "unknown job type"})

if __name__ == '__main__':
    print("Worker running!")
    run_job()

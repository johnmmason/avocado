import database, json
from psycopg2 import OperationalError
from jobs import q, get_job, update_job, save_plot
import analytics

@q.worker
def run_job(jid):
    job = get_job(jid)
    job_type = job['job_type']

    print("Accepted job " + job['job_id'] + ".")
    
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
  
            if job['plot_type'] == "box":
                
                update_job(job, {"status": "in progress"})
                plt = analytics.box_plot(job['cols'], job['params'])
                save_plot(jid, plt)
                update_job(job, {"status": "success", "img_id": jid})

            elif job['plot_type'] == "line":
                
                update_job(job, {"status": "in progress"})
                plt = analytics.line_plot(job['cols'], job['params'])
                save_plot(jid, plt)
                update_job(job, {"status": "success", "img_id": jid})

            elif job['plot_type'] == "bar":
                
                update_job(job, {"status": "in progress"})
                plt = analytics.bar_plot(job['cols'], job['params'])
                save_plot(jid, plt)
                update_job(job, {"status": "success", "img_id": jid})
                
            else:
                raise Exception("An unexpected error occured: invalid plot type")
            
        except Exception as error:
            update_job(job, {"status": "failed", "error": str(error)})

    elif job_type == "summary":

        # try:
        job['stats'] = analytics.summary(job['cols'])
        update_job(job, {"status": "success"})
        # except:
        #     update_job(job, {"status": "failed"})

if __name__ == '__main__':
    print("Worker running!")
    run_job()

from jobs import q, update_job
import time

@q.worker
def execute_job(jid):
    update_job(jid, 'start', {'job_type':'insert', 'status':'in_progress'})
    time.sleep(15)
    update_job(jid, 'end', {'job_type':'insert', 'status':'complete',)

execute_job()

from worker import run_job
import json

if __name__ == '__main__':    

    job = {
        "job_type": "insert",
        "status": "submitted",
        "data": {
            "week_id": 51,
            "week": "01/01/12",
            "price": 1.53,
            "volume": 8463.4,
            "total_4046": 6433.4,
            "total_4225": 3114.2,
            "total_4770": 143.5,
            "category": "conventional",
            "year": 2012,
            "region": "Atlanta"
        }
    }

    print( json.dumps(run_job(job), indent=4) )
    
    job = {
        "job_type": "query",
        "status": "submitted",
        "cols": ['id', 'price', 'region'],
        "params": [
            {
            "column": "year",
            "type": "equals",
            "value": 2012
            }
        ]
    }
    
    print ( json.dumps(run_job(job), indent=4) )

    job = {
        "job_type": "update",
        "status": "submitted",
        "params": [
            {
            "column": "year",
            "type": "equals",
            "value" : 2012
            }
        ],
        "data": {
            "volume": 9436.7,
            "category": "transitional"
        }
    }

    print( json.dumps(run_job(job), indent=4) )

    job = {
        "job_type": "delete",
        "status": "submitted",
        "params": [
            {
            "column": "year",
            "type": "equals",
            "value": 2012
            },
            {
            "column": "category",
            "type": "equals",
            "value": "transitional"
            }
        ]
    }

    print( json.dumps(run_job(job), indent =4) )

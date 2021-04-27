# avocado/worker

Currently, the following jobs are accepted:

## Insert

Note: all columns are required in the data field.

```
{
    "job_type": "insert",
    "status": "submitted",
    "data": {
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
}
```

## Query

The query job accepts a list of colums `cols` and a list of parameters `params`.

Each parameter must be defined with keys `{column, type, value}`.  Currently, the only supported type is `{equals}`.

```
{
    "job_type": "query",
    "status": "submitted",
    "cols": ["id", "price"],
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
```

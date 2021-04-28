# avocado/worker

Currently, the following jobs are accepted:

## Insert

The insert job type adds a single row to the database.

#### Requirements:

A parameter `data` with a key-value dictionary of all columns in the table and the values to be added.

#### Example:
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

The query job type retrieves a subset of the database matching given parameters.

#### Requirements:

The query job accepts a list of colums `cols` and a list of parameters `params`.

Each parameter must be defined with keys `{column, type, value}`.  Supported operators are `equals, greater_than, greater_equal, less_than, less_equal`.

#### Example:


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
        "column": "total_4046",
        "type": "less_equal",
        "value": 700
        }]
}
```

## Update

The update job type modifies a subset of the database matching given parameters.

#### Requirements:

The update job accepts a list of parameters `params` and new data `data`.

Each parameter must be defined with keys `{column, type, value}`.  Supported operators are `equals, greater_than, greater_equal, less_than, less_equal`.

#### Example:

```
{
    "job_type": "update",
    "status": "submitted",
    "params": [
        {
        "column": "year",
        "type": "equals",
        "value": 2012
        }
    ],
    "data": {
        "volume": 5,
        "category": "organic"
    }
}
```

## Delete

The delete job type removes all rows from the database which match given parameters.

#### Requirements:

The delete job accepts a list of parameters `params` and new data `data`.

Each parameter must be defined with keys `{column, type, value}`.  Supported operators are `equals, greater_than, greater_equal, less_than, less_equal`.

#### Examples:

```
{
    "job_type": "delete",
    "status": "submitted",
    "params": [{
        "column": "year",
        "type": "equals",
        "value": 2012
        },
        {
        "column": "category",
        "type": "equals",
        "value": "organic"
        }
    ]
}
```

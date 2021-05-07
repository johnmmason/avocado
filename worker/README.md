# avocado/worker

Each worker node retrieves and processes jobs from the Redis database, first in first out.  Each job is defined by a set of key-value pairs in JSON format and is assigned a unique job identifier when inserted into the database.  The job identifier can be used to track and retrieve the job upon completion or to diagnose a failed job.

Every job must have a supported `job_type` and all required parameters.

A job in the database might look like:

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

## Supported Job Types

The following job types are supported:

* Insert
* Query
* Update
* Delete
* Plot
* Summary

### Insert

The insert job type adds a single row to the database.

#### Requirements:

A parameter `data` with a key-value dictionary of all columns in the table and the values to be added.

| Key | Value |
| --- | ----- |
| data | A key-value dictionary of all columns in the table and the values to be added |

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

### Query

The query job type retrieves a subset of the database matching given parameters.

#### Requirements:

| Key | Value |
| --- | ----- |
| cols | A list of columns to return |
| params | A list with any number of query parameters. |

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

### Update

The update job type modifies a subset of the database matching given parameters.

#### Requirements:

| Key | Value |
| --- | ----- |
| params | A list with any number of query parameters. |
| data | A key-value dictionary of columns to be updated |

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

### Delete

The delete job type removes all rows from the database which match given parameters.

#### Requirements:

The delete job accepts a list of parameters `params`.

| Key | Value |
| --- | ----- |
| params | A list with any number of query parameters |
| data | A key-value dictionary of columns to be updated |

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


### Plot

The plot job type creates a basic plot defined by the given parameters:

#### Requirements:

| Key | Value |
| --- | ----- |
| plot_type | A string, one of `{bar, line, box}`. |
| cols | A list of exactly two column names in the format `[ x-axis, y-axis ]`. |
| params | A list with any number of query parameters. See below. |

Each parameter must be defined with keys `{column, type, value}`.  Supported operators are `equals, greater_than, greater_equal, less_than, less_equal`.

#### Example:

```
{
    "job_type": "plot",
    "plot_type": "box",
    "status": "submitted",
    "cols": ["year", "price"],
    "params": [{
        "column": "year",
        "type": "greater_than",
        "value": 2012
        }]
}
```

Once complete, the plot can be accessed using the assigned job id or image id:

In your browser, navigate to `https://isp-proxy.tacc.utexas.edu/phart/download/<jobid>`.

### Summary

The summary job type returns the summary statistics mean, median, std deviation, 25% quantile, 50% quantile, 75% quantile, and count for each specified column.

#### Requirements:

| Key | Value |
| --- | ----- |
| cols | A list of column names. |

#### Example:

```
{
    "job_type": "summary",
    "status": "submitted",
    "cols": ["year", "price"]
}
```

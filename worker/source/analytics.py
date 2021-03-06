import psycopg2
import pandas as pd
import os
import json
from database import DB_COLUMNS, __build_query
import matplotlib.pyplot as plt
import seaborn as sns

PG_HOST = os.environ['PG_HOST']
PG_USER = os.environ['PG_USER']
PG_PASSWORD = os.environ['PG_PASSWORD']
PG_DATABASE = os.environ['PG_DATABASE']

SELECT_QUERY = "SELECT {},{} FROM avocado"

def _load_df(query, cols):

    conn = psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cursor = conn.cursor()

    try:
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cursor.close()
        conn.close()
        return None

    tupples = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(tupples, columns=cols)
    return df

def bar_plot(columns, params=[]):

    assert len(columns) == 2, 'Invalid number of columns for plot type bar'

    for column in columns:
        assert column in DB_COLUMNS, 'Invalid column name ' + column
    
    X_name = columns[0]
    Y_name = columns[1]

    df = _load_df(SELECT_QUERY.format(X_name, Y_name) + __build_query(params), [X_name, Y_name])

    X = df[X_name]
    Y = df[Y_name]
    
    plt.bar(X, Y)

    plt.title(Y_name + " by " + X_name)
    plt.xlabel(X_name)
    plt.ylabel(Y_name)

    return plt

def line_plot(columns, params=[]):

    assert len(columns) == 2, 'Invalid number of columns for plot type line'

    for column in columns:
        assert column in DB_COLUMNS, 'Invalid column name ' + column
    
    X_name = columns[0]
    Y_name = columns[1]
    
    df = _load_df(SELECT_QUERY.format(X_name, Y_name) + __build_query(params) + " ORDER BY " + X_name + " ASC", [X_name, Y_name])

    X = df[X_name]
    Y = df[Y_name]

    plt.title(Y_name + " by " + X_name)
    plt.xlabel(X_name)
    plt.ylabel(Y_name)

    plt.plot(X, Y)

    return plt

def box_plot(columns, params=[]):

    assert len(columns) == 2, 'Invalid number of columns for plot type box'

    for column in columns:
        assert column in DB_COLUMNS, 'Invalid column name ' + column
    
    X_name = columns[0]
    Y_name = columns[1]
    
    df = _load_df(SELECT_QUERY.format(X_name, Y_name) + __build_query(params), [X_name, Y_name])

    X = df[X_name]
    Y = df[Y_name]

    sns.set_theme(style='whitegrid')
    ax = sns.boxplot(x=X, y=Y)

    plt.title(Y_name + " by " + X_name)
    plt.xlabel(X_name)
    plt.ylabel(Y_name)
    
    return plt

def summary(columns):
    
    assert type(columns) == list

    df = _load_df("SELECT * FROM avocado", DB_COLUMNS)

    stats = {}
    
    for column in columns:

        assert column in DB_COLUMNS, 'Invalid column name ' + column
        
        stats[column] = {
            "mean": df[column].mean(),
            "median": df[column].median(),
            "std": df[column].std(),
            "q25": df[column].quantile(q=.25),
            "q50": df[column].quantile(q=.50),
            "q75": df[column].quantile(q=.75),
            "count": df.shape[0]
        }

    return stats

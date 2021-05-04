import psycopg2
from psycopg2.extensions import AsIs
import json
import os

PG_HOST = os.environ['PG_HOST']
PG_USER = os.environ['PG_USER']
PG_PASSWORD = os.environ['PG_PASSWORD']
PG_DATABASE = os.environ['PG_DATABASE']

DB_COLUMNS = ['id', 'week_id', 'week', 'price', 'volume', 'total_4046', 'total_4225', 'total_4770', 'category', 'year', 'region']

def __map_dict(rows, cols):
    rows_list = []
    
    for row in rows:
        row_dict = {}
        for i in range(0, len(cols)):
            row_dict[cols[i]] = row[i]
        rows_list.append(row_dict)
    return rows_list

def __build_query(params):

    KEY_QUERY = ''
    
    first_key = True
    for param in params:
        if first_key:
            KEY_QUERY = ' WHERE '
            first_key = False
        else:
            KEY_QUERY = KEY_QUERY + ' AND '
            
        if param['type'] == 'equals':
            KEY_QUERY = KEY_QUERY + param['column'] + " = '" + str(param['value']) + "'"
        elif param['type'] == 'greater_than':
            KEY_QUERY = KEY_QUERY + param['column'] + " > '" + str(param['value']) + "'"
        elif param['type'] == 'greater_equal':
            KEY_QUERY = KEY_QUERY + param['column'] + " >= '" + str(param['value']) + "'"
        elif param['type'] == 'less_than':
            KEY_QUERY = KEY_QUERY + param['column'] + " < '" + str(param['value']) + "'"
        elif param['type'] == 'less_equal':
            KEY_QUERY = KEY_QUERY + param['column'] + " <= '" + str(param['value']) + "'"
        else:
            raise Exception

    return KEY_QUERY

def insert(data):
    conn = psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cursor = conn.cursor()

    columns = data.keys()
    values = [ data[column] for column in columns ]

    SQL = 'INSERT INTO avocado (%s) VALUES %s'

    cursor.execute(SQL, (AsIs(','.join(columns)), tuple(values)))
    conn.commit()
    
    cursor.close()
    conn.close()
    
def get(cols, params):
    conn = psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cursor = conn.cursor()
    
    SQL = 'SELECT {} FROM avocado'.format(AsIs(','.join(cols)))
    SQL = SQL + __build_query(params)

    cursor.execute(SQL)
    data = __map_dict(cursor.fetchall(), cols)

    cursor.close()
    conn.commit()
    conn.close()
    
    return data

def update(data, params):
    conn = psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cursor = conn.cursor()

    SQL = 'UPDATE avocado SET '
    
    keys = list( data.keys() )
    for i in range(0, len(data)):
        SQL = SQL + keys[i] + " = '" + str(data[ keys[i] ]) + "'"
        if i < len(data)-1:
            SQL = SQL + ", "
        
    SQL = SQL + __build_query(params)

    cursor.execute(SQL)

    cursor.close()
    conn.commit()
    conn.close()

def delete(params):
    conn = psycopg2.connect(
        host=PG_HOST,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cursor = conn.cursor()
    
    SQL = 'DELETE FROM avocado'
    SQL = SQL + __build_query(params)

    cursor.execute(SQL)

    cursor.close()
    conn.commit()
    conn.close()
    

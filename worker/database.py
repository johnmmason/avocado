import psycopg2
from psycopg2.extensions import AsIs

PG_HOST = 'localhost'
PG_USER = 'avocado'
PG_PASSWORD = 'avocado'
PG_DATABASE = 'avocado'

DB_ROWS = ['id', 'week_id', 'price', 'volume', 'total_4046', 'total_4225', 'total_4770', 'category', 'year', 'region']

def __map_dict(rows, cols):
    rows_list = []
    
    for row in rows:
        print( type(row) )
        row_dict = {}
        for i in range(0, len(cols)):
            row_dict[cols[i]] = row[i]
        rows_list.append(row_dict)
    return rows_list

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

    if cols:
        pass
    else:
        cols = '*'
    
    SQL = 'SELECT {} FROM avocado'.format(AsIs(','.join(cols)))

    first_key = True
    for param in params:
        if first_key:
            KEY_QUERY = ' WHERE '
            first_key = False
        else:
            KEY_QUERY = KEY_QUERY + ' AND '
        if param['type'] == 'equals':
            KEY_QUERY = KEY_QUERY + param['column'] + " = " + str(param['value'])
        else:
            raise Exception

    cursor.execute(SQL+KEY_QUERY)
    data = __map_dict(cursor.fetchall(), cols)

    cursor.close()
    conn.commit()

    return data

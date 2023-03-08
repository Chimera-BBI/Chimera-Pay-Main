import psycopg2.pool

from Chimere_Pay import app

aws_keys = app.config['aws_keys']

pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                            host=aws_keys["host"],
                                            port=aws_keys["port"],
                                            database=aws_keys["database"],
                                            user=aws_keys["user"],
                                            password=aws_keys["password"])

def execute_enter_data(table_name:str, column_names:list, values) -> int:
    """
    Inserts data into a table in a PostgreSQL database.
    
    Parameters:
    - table_name: str, name of the table to insert data into
    - column_names: list, names of the columns to insert data into, separated by commas
    - values: list of str, values to insert into the table, in the same order as the column names
    
    Returns:
    - 1 if insertion was successful, -1 if there was an error
    
    Example:
    execute_enter_data('users', 'name, email', ['John', 'john@example.com'])
    """

    # pool = app.config["Connection Pool"]

    # format the column names and values for the query
    columns_to_enter = ",".join(map(str,column_names))
    values_to_enter  = ",".join(map(lambda x: rf"'{x}'",values))
    
    # build the base query
    query = f"insert into {table_name} ({columns_to_enter}) values ({values_to_enter})"

    # try to execute the query, return 1 if successful, -1 if there's an error
    try:
        # Get a connection from the pool
        conn = pool.getconn()
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query)
            return 1
    except (Exception, psycopg2.Error) as error :
        print(query)
        print ("Error while inserting data from PostgreSQL -->", error)
        return -1

    finally:
        # Return the connection to the pool
        if(conn):
            pool.putconn(conn)
            print("PostgreSQL connection returned to the pool")



def execute_get_data(table_name:str, column_names:list = None, where_dict:dict = None) -> list:
    """
    Fetches data from a table in a PostgreSQL database.
    
    Parameters:
    - table_name: str, name of the table to fetch data from
    - column_names: list of str, names of the columns to return data from (defaults to '*', all columns)
    - where_dict: dict, a dictionary with keys as column names and values as the desired values to filter by
    
    Returns:
    - list of tuples, each tuple representing a row of data
    
    Example:
    execute_get_data('users', ['name', 'email'], {'name': 'John'})
    """

    # pool = app.config["Connection Pool"]


    # format the column names for the query
    if column_names != None:
        columns_to_return = ",".join(map(str,column_names))
    else:
        columns_to_return = "*"
    # build the base query
    query = f"select {columns_to_return} from {table_name}"
    
    # add a WHERE clause to the query if specified
    if where_dict!=None:
        where_clause    = " AND ".join(map(lambda x : f"{x} like '{where_dict[x]}'",where_dict))
        query           = query + " where "+where_clause
    
    # try to execute the query, return the data if successful, -1 if there's an error
    try:
        # Get a connection from the pool
        conn = pool.getconn()
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query)
            record = cursor.fetchall()
            return record

    except (Exception, psycopg2.Error) as error :
        print(query)
        print ("Error while fetching data from PostgreSQL -->", error)
        return -1

    finally:
        # Return the connection to the pool
        if(conn):
            pool.putconn(conn)
            print("PostgreSQL connection returned to the pool")

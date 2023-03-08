import psycopg2.pool

from Chimere_Pay import app

aws_keys = app.config['aws_keys']

pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                            host=aws_keys["host"],
                                            port=aws_keys["port"],
                                            database=aws_keys["database"],
                                            user=aws_keys["user"],
                                            password=aws_keys["password"])

def execute_enter_data( table_name:str,
                        input_dict:dict, 
                        # column_names:list,
                        # values:list,
                        update_table:bool = False,
                        where_dict:dict = None):
                        
    """The `execute_enter_data` function is used to either insert new data or update existing data in a PostgreSQL database table. The function takes in the following arguments:

        - `table_name` : a string representing the name of the table where data is to be inserted/updated.
        - `input_dict` : a dictionary containing the column names as keys and the values to be inserted/updated as values.
        - `update_table` : a boolean indicating whether data is to be updated in the table or not. Default is False.
        - `where_dict` : a dictionary containing the column names and values to be used in the WHERE clause for updating data.

        The function returns `1` if the query was executed successfully, `-1` otherwise.
        
        Example usage for inserting data:

        table_name = 'students'
        input_dict = {'name': 'John', 'age': 25, 'gender': 'M'}
        execute_enter_data(table_name, input_dict)

        Example usage for updating data:

        table_name = 'students'
        input_dict = {'name': 'John Doe', 'age': 26, 'gender': 'M'}
        where_dict = {'name': 'John', 'age': 25}
        execute_enter_data(table_name, input_dict, update_table=True, where_dict=where_dict)
    """
    if update_table:

        set_query = " , ".join(map(lambda x: rf"{x} = {input_dict[x]}",input_dict.keys()))

        query = f"UPDATE {table_name} SET {set_query}"

        if where_dict!=None:
            where_clause    = " AND ".join(map(lambda x : f"{x} like '{where_dict[x]}'",where_dict))
            query           = query + " where "+where_clause
        
        
    else:
    
        columns_to_enter = ",".join(map(str,input_dict.keys()))
        values_to_enter  = ",".join(map(lambda x: rf"{x}",input_dict.values()))    
        
        # columns_to_enter = ",".join(map(str,column_names))
        # values_to_enter  = ",".join(map(lambda x: rf"'{x}'",values))    
        
        #base query                        
        query = f"insert into {table_name} ({columns_to_enter}) values ({values_to_enter})"


    # return query
    try:
        # Get a connection from the pool
        conn = pool.getconn()
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query)
            return 1
            # record = await cursor.fetchone()
            # return jsonify({"id": record[0], "name": record[1], "cost": record[2]})

    except (Exception, psycopg2.Error) as error :
        print(query)
        print ("Error while inserting data from PostgreSQL -->", error)
        return -1

    finally:
        # Return the connection to the pool
        if(conn):
            pool.putconn(conn)
            print("PostgreSQL connection returned to the pool")


def execute_get_data(table_name:str, 
                    column_names:dict = None, 
                    where_dict:dict = None):
    
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

    if column_names != None:
        columns_to_return = ",".join(map(str,column_names))
    else:
        columns_to_return = "*"
    #base query                        
    query = f"select {columns_to_return} from {table_name}"

    if where_dict!=None:
        where_clause    = " AND ".join(map(lambda x : f"{x} like '{where_dict[x]}'",where_dict))
        query           = query + " where "+where_clause
    # return query

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
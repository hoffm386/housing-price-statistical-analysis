import psycopg2

def create_database():
    """
    This function assumes that you have an existing database called `postgres`
    without any username/password required to access it.  Then it creates a new
    database called `housing_data`
    """
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True # it seems this mode is needed to make a db
    cursor = conn.cursor()
    CREATE_DATABASE_QUERY = "CREATE DATABASE housing_data;"
    cursor.execute(CREATE_DATABASE_QUERY)
    conn.close()

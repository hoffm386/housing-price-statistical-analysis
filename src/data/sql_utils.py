import psycopg2
import pandas as pd
import os

def create_database():
    """
    This function assumes that you have an existing database called `postgres`
    without any username/password required to access it.  Then it creates a new
    database called `housing_data`
    """
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True # it seems this mode is needed to make a db
    conn.set_isolation_level(0) # also this for dropping db

    execute_sql_script(conn, "01_drop_old_database.sql")
    execute_sql_script(conn, "02_create_new_database.sql")

    conn.close()

def create_sales_table(conn):
    execute_sql_script(conn, "03_create_sales_table.sql")

def create_buildings_table(conn):
    execute_sql_script(conn, "04_create_buildings_table.sql")

def create_parcels_table(conn):
    execute_sql_script(conn, "05_create_parcels_table.sql")

def copy_csv_to_sales_table(conn, sales_csv_file):
    # skip the header row
    next(sales_csv_file)
    copy_expert_psql_script(conn, "06_copy_sales_csv_to_table.psql", sales_csv_file)

def copy_csv_to_buildings_table(conn, buildings_csv_file):
    # skip the header row
    next(buildings_csv_file)
    copy_expert_psql_script(conn, "07_copy_buildings_csv_to_table.psql", buildings_csv_file)

def copy_csv_to_parcels_table(conn, parcels_csv_file):
    # skip the header row
    next(parcels_csv_file)
    copy_expert_psql_script(conn, "08_copy_parcels_csv_to_table.psql", parcels_csv_file)

def create_tables():
    conn = psycopg2.connect(dbname="housing_data")

    create_sales_table(conn)
    create_buildings_table(conn)
    create_parcels_table(conn)

    conn.close()

def copy_csv_files(sales_csv_file, buildings_csv_file, parcels_csv_file):
    conn = psycopg2.connect(dbname="housing_data")

    copy_csv_to_sales_table(conn, sales_csv_file)
    copy_csv_to_buildings_table(conn, buildings_csv_file)
    copy_csv_to_parcels_table(conn, parcels_csv_file)

    conn.close()

def create_database_and_tables():
    create_database()
    create_tables()

def create_sales_df():
    conn = psycopg2.connect(dbname="housing_data")

    SALES_DF_QUERY = """
        SELECT
            CONCAT(sales.Major, sales.Minor) AS PIN,     -- parcel id number
            sales.SalePrice,
            sales.DocumentDate,
            CASE
                WHEN parcels.WfntLocation > 0            -- 1-9 indicate particular bodies of water
                    THEN TRUE
                ELSE                                     -- I infer that 0 means no waterfront
                    FALSE
            END as WfntLocation,
            buildings.SqFtTotLiving
        FROM sales                                       -- start the join with sales bc sale price is target
        INNER JOIN parcels ON (                          -- parcel major + minor is the unique identifier
            parcels.Major = sales.Major                  -- (parcels are the things being sold in the sales)
            AND parcels.Minor = sales.Minor
        )
        INNER JOIN buildings ON (                        -- building belongs to one parcel
            buildings.Major = parcels.Major              -- parcel can have many buildings (unclear how often)
            AND buildings.Minor = parcels.Minor
        )
        WHERE (
            date_part('year', sales.DocumentDate) = 2018 -- 2018 is the specified year
            AND sales.SalePrice > 0                      -- assume that sale price of 0 is bad data
        )
        ORDER BY sales.DocumentDate;
    """

    sales_df = pd.read_sql_query(SALES_DF_QUERY, conn)
    return sales_df

def open_sql_script(script_filename):
    """
    Given a file path, open the file and return its contents
    We assume that the file path is always inside the sql directory
    """
    dir = os.path.dirname(__file__)
    relative_filename = os.path.join(dir, 'sql', script_filename)

    file_obj = open(relative_filename, 'r')
    file_contents = file_obj.read()
    file_obj.close()

    return file_contents

def execute_sql_script(conn, script_filename):
    """
    Given a DB connection and a file path to a SQL script, open up the SQL
    script and execute it
    """
    file_contents = open_sql_script(script_filename)
    cursor = conn.cursor()
    cursor.execute(file_contents)
    conn.commit()

def copy_expert_psql_script(conn, script_filename, csv_file):
    """
    Given a DB connection and a file path to a PSQL script, open up the PSQL
    script and use it to run copy_expert
    """
    file_contents = open_sql_script(script_filename)
    cursor = conn.cursor()
    cursor.copy_expert(file_contents, csv_file)
    conn.commit()

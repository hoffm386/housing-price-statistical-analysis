import psycopg2

def create_database():
    """
    This function assumes that you have an existing database called `postgres`
    without any username/password required to access it.  Then it creates a new
    database called `housing_data`
    """
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True # it seems this mode is needed to make a db
    conn.set_isolation_level(0) # also this for dropping db
    cursor = conn.cursor()
    DROP_OLD_DATABASE_QUERY = "DROP DATABASE housing_data;"
    cursor.execute(DROP_OLD_DATABASE_QUERY)
    CREATE_DATABASE_QUERY = "CREATE DATABASE housing_data;"
    cursor.execute(CREATE_DATABASE_QUERY)
    conn.close()

def create_sales_table(conn):
    CREATE_SALES_TABLE_QUERY = """
        DROP TABLE IF EXISTS sales;
        CREATE TABLE sales (
        ExciseTaxNbr       INT,
        Major              CHAR(6),
        Minor              CHAR(4),
        DocumentDate       DATE,
        SalePrice          INT,
        RecordingNbr       CHAR(14),
        Volume             CHAR(3),
        Page               CHAR(3),
        PlatNbr            CHAR(6),
        PlatType           CHAR(1),
        PlatLot            CHAR(14),
        PlatBlock          CHAR(7),
        SellerName         TEXT,
        BuyerName          TEXT,
        PropertyType       INT,
        PrincipalUse       INT,
        SaleInstrument     INT,
        AFForestLand       CHAR(1),
        AFCurrentUseLand   CHAR(1),
        AFNonProfitUse     CHAR(1),
        AFHistoricProperty CHAR(1),
        SaleReason         INT,
        PropertyClass      INT,
        SaleWarning        TEXT
        );
    """
    cursor = conn.cursor()
    cursor.execute(CREATE_SALES_TABLE_QUERY)
    conn.commit()

def copy_csv_to_sales_table(conn, sales_csv_file):
    # skip the header row
    next(sales_csv_file)

    COPY_SALES_QUERY = """COPY sales FROM STDIN WITH (FORMAT CSV)"""
    cursor = conn.cursor()
    cursor.copy_expert(COPY_SALES_QUERY, sales_csv_file)
    conn.commit()

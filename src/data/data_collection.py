import requests
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
from sql_utils import create_database_and_tables, copy_csv_files

def download_zipfile(URL):
    """
    Given a URL for a .zip, download and unzip the .zip file
    """
    response = requests.get(URL)
    content_as_file = BytesIO(response.content)
    zip_file = ZipFile(content_as_file)
    return zip_file

def open_csv(zip_file, csv_name):
    """
    Given an unzipped .zip file and the name of a CSV inside of it, 
    extract the CSV and return the relevant file
    """
    csv_file_bytes = zip_file.open(csv_name)
    # it seems we have to open the .zip as bytes, but CSV reader requires text
    csv_file_text = TextIOWrapper(csv_file_bytes, encoding="ISO-8859-1")
    return csv_file_text

def collect_data(URL, csv_name):
    """
    Helper function used to collect all three CSV files
    """
    zip_file = download_zipfile(URL)
    csv_file = open_csv(zip_file, csv_name)
    # return both so we can safely close them at the end
    return zip_file, csv_file


def collect_sales_data():
    SALES_URL = "https://aqua.kingcounty.gov/extranet/assessor/Real%20Property%20Sales.zip"
    SALES_CSV_NAME = "EXTR_RPSale.csv"
    sales_zip_file, sales_csv_file = collect_data(SALES_URL, SALES_CSV_NAME)
    return sales_zip_file, sales_csv_file

def collect_buildings_data():
    BUILDINGS_URL = "https://aqua.kingcounty.gov/extranet/assessor/Residential%20Building.zip"
    BUILDINGS_CSV_NAME = "EXTR_ResBldg.csv"
    buildings_zip_file, buildings_csv_file = collect_data(BUILDINGS_URL, BUILDINGS_CSV_NAME)
    return buildings_zip_file, buildings_csv_file

def collect_parcels_data():
    PARCELS_URL = "https://aqua.kingcounty.gov/extranet/assessor/Parcel.zip"
    PARCELS_CSV_NAME = "EXTR_Parcel.csv"
    parcels_zip_file, parcels_csv_file = collect_data(
        PARCELS_URL, PARCELS_CSV_NAME)
    return parcels_zip_file, parcels_csv_file

def collect_all_data_files():
    return collect_sales_data(), collect_buildings_data(), collect_parcels_data()

def load_into_sql(sales_files, buildings_files, parcels_files):
    sales_zip_file, sales_csv_file = sales_files
    buildings_zip_file, buildings_csv_file = buildings_files
    parcels_zip_file, parcels_csv_file = parcels_files

    copy_csv_files(sales_csv_file, buildings_csv_file, parcels_csv_file)

    sales_zip_file.close()
    sales_csv_file.close()
    buildings_zip_file.close()
    buildings_csv_file.close()
    parcels_zip_file.close()
    parcels_csv_file.close()

def download_data_and_load_into_sql():
    create_database_and_tables()
    sales_files, buildings_files, parcels_files = collect_all_data_files()
    load_into_sql(sales_files, buildings_files, parcels_files)

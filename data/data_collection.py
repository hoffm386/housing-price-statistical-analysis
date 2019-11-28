import requests
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
from csv import DictReader

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
    # it seems we have to open the .zip as bytes, but DictReader requires text
    csv_file_text = TextIOWrapper(csv_file_bytes)
    return csv_file_text

def collect_data(URL, csv_name):
    """
    Helper function used to collect all three CSV files
    """
    zip_file = download_zipfile(URL)
    csv_file = open_csv(zip_file, csv_name)
    # return both so we can safely close them at the end
    return zip_file, csv_file

def collect_parcels_data():
    PARCELS_URL = "https://aqua.kingcounty.gov/extranet/assessor/Parcel.zip"
    PARCELS_CSV_NAME = "EXTR_Parcel.csv"
    parcels_zip_file, parcels_csv_file = collect_data(PARCELS_URL, PARCELS_CSV_NAME)
    return parcels_zip_file, parcels_csv_file

def collect_sales_data():
    SALES_URL = "https://aqua.kingcounty.gov/extranet/assessor/Real%20Property%20Sales.zip"
    SALES_CSV_NAME = "EXTR_RPSale.csv"
    sales_zip_file, sales_csv_file = collect_data(SALES_URL, SALES_CSV_NAME)
    return sales_zip_file, sales_csv_file

def collect_building_data():
    BUILDINGS_URL = "https://aqua.kingcounty.gov/extranet/assessor/Residential%20Building.zip"
    BUILDINGS_CSV_NAME = "EXTR_ResBldg.csv"
    buildings_zip_file, buildings_csv_file = collect_data(BUILDINGS_URL, BUILDINGS_CSV_NAME)
    return buildings_zip_file, buildings_csv_file



# Housing Price Statistical Analysis
This repository was created for educational purposes, as an example solution to Flatiron School's [Module 2 Final Project](https://github.com/learn-co-students/dsc-mod-2-project-seattle-ds-102819)

The overarching goal of this project is to build a linear regression model to make inferences about housing prices in King County in 2018.  Unlike with a predictive framing, the main emphasis is on generating reliable coefficients, so it is important to make sure none of the assumptions of a linear regression have been violated.

## Directory Structure

This directory structure is inspired by [cookiecutter data science](https://github.com/drivendata/cookiecutter-data-science)
```
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering)
│   │                     followed by the topic of the notebook, e.g.
│   │                     01_data_collection_exploration.ipynb
│   └── exploratory    <- Raw, flow-of-consciousness, work-in-progress notebooks
│
├── src                <- Source code for use in this project
│   ├── data           <- Scripts to download and query data
│   │   ├── data_collection.py
│   │   └── sql_utils.py
│   │
│   ├── modeling       <- Scripts to build and evaluate models
│   │   ├── model_evaluation.py
│   │   └── modeling.py
│   │
│   └── __init__.py    <- Makes src a Python module
│
├── .gitignore         <- Keep some things out of source control
├── environment.yml    <- The requirements file for reproducing the analysis environment with conda
├── README.md          <- The top-level README for developers using this project.
├── requirements.txt   <- The requirements file for reproducing the analysis environment with pip
└── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
```

## Setup Instructions

### Prerequisites

This project assumes that you have installed `pip` or `conda` as well as PostgreSQL, with a PostgreSQL default database name of "postgres".  It also requires that you have an internet connection, to download the required Python packages as well as the housing data from the King County website.  The code in this project has only been tested on a Mac computer, although it likely will work on other operating systems as well.

### Installing Required Packages

#### Preferred Environment Setup: `conda`

If you have `conda` on your system, run `conda env create -f environment.yml` in the terminal, and type `y` when prompted.  Once the download is complete, run `conda activate mod2-project-env` to install all necessary packages.

#### Alternative Environment Setup: `pip`

It is still recommended that you use some kind of environment manager to isolate these packages from your base environment, even if you do not have `conda`.

If you have `pip` on your system, run `pip install -r requirements.txt` to install all necessary packages.

### Jupyter Lab Setup

The visualization code in the notebooks assumes that you have notebook extensions to render them inline within Jupyter Lab.

To install these extensions (after installing required packages), run:
```
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-matplotlib
jupyter nbextension enable --py widgetsnbextension
```

## Downloading the Data

You may have noticed that there is no `data/` directory.  This is on purpose!  This repository's code downloads data from the King County website and loads it directly into a PostgreSQL database, without saving CSV files to the disk in the interim.

To load the data into your local PostgreSQL server, open up Python within the repository (command-line REPL or notebook) and run:
```
from src.data import data_collection
data_collection.download_data_and_load_into_sql()
```

This may take up to a couple minutes, depending on your internet connection and processing power.

To test that the download worked while still in Python, try running a query like:
```
import psycopg2
import pandas as pd
```
```
conn = psycopg2.connect(dbname="housing_data")
pd.read_sql_query("SELECT * FROM sales LIMIT 5;", conn)
```
```
conn.close()
```

Because it is loaded into a PostgreSQL database, you can also query it with any client you prefer, not just `psycopg2`.  For example, if you prefer a command-line interface without Python, you can use the `psql` CLI tool.

## Developing `src` Files

In order to have the library code in the `src` directory available to all files, you will need to install it as a package.  By default, you have installed the version from [@hoffm386](https://github.com/hoffm386), the original author of this repository.  But if you want to see changes you have made reflected locally, you will need to install your local copy.  To do this, run `pip install -e .` in the terminal.

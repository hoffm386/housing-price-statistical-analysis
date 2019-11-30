import statsmodels.api as sm
from src.data import sql_utils

def build_linreg_model():
    sales_df = sql_utils.create_sales_df()

    # perform transformations in preparation for modeling
    transform_wfntlocation(sales_df)

    # extract target (sale price)
    y = sales_df["saleprice"]

    # extract features
    X = sales_df[[
        "wfntlocation", 
        "sqfttotliving"
        ]]
    X = sm.add_constant(X)

    model = sm.OLS(y, X)
    return model


def transform_wfntlocation(sales_df):
    """
    Transforms the Waterfront Location column into an integer in preparation
    for modeling
    
    The SQL query returns True and False for the Waterfront Location query,
    which is a more human-understandable description.  But a linear regression
    model doesn't know what a boolean is, so we need to cast them to int.
    """
    sales_df["wfntlocation"] = sales_df["wfntlocation"].astype(int)

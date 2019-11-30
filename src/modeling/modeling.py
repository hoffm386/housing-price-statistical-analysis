import statsmodels.api as sm
from src.data import sql_utils
from src.modeling import model_evaluation

def build_and_evaluate_model():
    """
    Complete "pipeline" from reading the data from SQL, selecting and
    transforming features, building a model, and evaluating whether the model
    violates the assumptions of a linear regression
    """
    y, X_without_constant, X = create_linreg_model_inputs()
    fit_and_evaluate_model_from_inputs(y, X_without_constant, X)

def create_linreg_model_inputs():
    """
    Read the sales dataframe in from SQL, perform transformations on columns,
    return relevant columns for linear regression model
    """
    sales_df = sql_utils.create_sales_df()

    # perform transformations in preparation for modeling
    transform_wfntlocation(sales_df)

    # extract target (sale price)
    y = sales_df["saleprice"]

    # extract features
    X_without_constant = sales_df[[
        "wfntlocation", 
        "sqfttotliving"
        ]]
    X = sm.add_constant(X_without_constant)
    return y, X_without_constant, X

def fit_and_evaluate_model_from_inputs(y, X_without_constant, X):
    """
    Given y (target variable) and X (with and without constant term),
    build a linear regression model and run tests for model assumptions
    """
    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())

    y_hat = results.predict()

    print("\nPerforming Linearity Checks\n")
    model_evaluation.perform_linearity_checks(X_without_constant, y, y_hat, results)

    print("\nPerforming Independence Checks\n")
    model_evaluation.perform_independence_checks(X)

    print("\nPerforming Homoscedasticity Checks\n")
    model_evaluation.perform_homoscedasticity_checks(y, y_hat, X_without_constant)

    print("\nPerforming Normality Checks\n")
    model_evaluation.perform_normality_checks(results)

def transform_wfntlocation(sales_df):
    """
    Transforms the Waterfront Location column into an integer in preparation
    for modeling
    
    The SQL query returns True and False for the Waterfront Location query,
    which is a more human-understandable description.  But a linear regression
    model doesn't know what a boolean is, so we need to cast them to int.
    """
    sales_df["wfntlocation"] = sales_df["wfntlocation"].astype(int)

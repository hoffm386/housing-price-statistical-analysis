import statsmodels.api as sm
from statsmodels.stats.diagnostic import linear_rainbow, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.stats import kstest

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

################################################################################
#  All-in-one "drivers" to check linear regression assumptions
################################################################################

def perform_linearity_checks(X_without_constant, y, y_hat, results):
    visualize_feature_linearity(X_without_constant, y)
    visualize_overall_linearity(y, y_hat)
    print(statistically_analyze_linearity(results))

def perform_independence_checks(X):
    print(visualize_statistical_independence(X))
    print(statistically_analyze_independence(X))

def perform_homoscedasticity_checks(y, y_hat, X_without_constant):
    visualize_homoscedasticity(y, y_hat)
    print(statistically_analyze_homoscedasticity(y, y_hat, X_without_constant))

def perform_normality_checks(results):
    visualize_normality(results)
    print(statistically_analyze_normality(results))

################################################################################
#  Visualizations for checking linear regression assumptions
#
#  Some of them produce figures with PyPlot, others return dataframes that
#  need to be printed (e.g. in a notebook)
################################################################################

def visualize_feature_linearity(X_without_constant, y):
    """
    For each feature, generate a scatter plot of the feature vs. the target
    """
    num_features = X_without_constant.shape[1]
    _, ax = plt.subplots(num_features)

    for index, feature in enumerate(X_without_constant.columns):
        ax[index].scatter(
            x=X_without_constant[feature],
            y=y,
            color="blue",
            alpha=0.2)
        ax[index].set(xlabel=feature, ylabel="Sale Price")
    plt.show()

def visualize_overall_linearity(y, y_hat):
    """
    Generate a scatter plot of predicted vs. actual sales price
    """
    _, ax = plt.subplots()

    # plot predicted vs actual
    ax.scatter(x=y_hat, y=y, color="blue", alpha=0.2)

    # plot the line where predicted equals actual
    # TODO: add a legend explaining the line
    x_vals = y_vals = np.array(ax.get_xlim())
    ax.plot(x_vals, y_vals, '--')

    ax.set(xlabel="Predicted Price", ylabel="Actual Price")
    plt.show()

def visualize_statistical_independence(X):
    """
    Create a dataframe that shows the VIF factor for each feature
    """
    num_features = X.shape[1]
    feature_indices = range(num_features)
    rows = X.values

    vif = pd.DataFrame()
    vif["VIF Factor"] = [variance_inflation_factor(
        rows, i) for i in feature_indices]
    vif["features"] = X.columns
    return vif

def visualize_homoscedasticity(y, y_hat):
    """
    Create a scatter plot of predicted price vs. residuals
    """
    _, ax = plt.subplots()
    ax.scatter(x=y_hat, y=y-y_hat, color="blue", alpha=0.2)
    ax.set(xlabel="Predicted Sale Price",
           ylabel="Residuals (Actual - Predicted Sale Price)")
    plt.show()

def visualize_normality(results):
    """
    Create a Q-Q plot comparing the theoretical and actual quantiles
    """
    _, ax = plt.subplots()
    prob_plot = sm.ProbPlot(results.resid)
    prob_plot.qqplot(line="s", ax=ax)
    plt.show()

################################################################################
#  Numeric statistical assessments of whether linear regression assumptions
#  have been met
#
#  For now I'm making a verbose (gives a string description) and a concise
#  (just the relevant numbers) version of each, where the verbose version
#  depends on the concise version
################################################################################

def statistically_analyze_linearity(results):
    """
    Check the linearity assumption of a linear regression model
    Return a message and a p-value describing the result
    """
    rainbow_p_value = calculate_linear_rainbow_p_value(results)

    if (rainbow_p_value < 0.05):
        return "Violates the linearity assumption according to the rainbow test", rainbow_p_value
    else:
        return "Does not violate the linearity assumption according to the rainbow test", rainbow_p_value

def calculate_linear_rainbow_p_value(results):
    """
    Runs a rainbow diagnostic test from statsmodels
    The null hypothesis is that the model is linearly predicted by the features,
    alternative hypothesis is that it is not.  Thus returning a low p-value
    means that the current model violates the linearity assumption.
    """
    # for now we discard the statistic itself, just use the p-value
    _, p_value = linear_rainbow(results)
    return p_value

def statistically_analyze_independence(X):
    """
    Check all of the features to make sure they are not too collinear
    Return a message and a dictionary of all features that are too collinear
    """
    vif_factors = calculate_vif_factors(X)
    too_high_vif_dict = {}

    for index, factor in enumerate(vif_factors):
        if (factor > 10):
            too_high_vif_dict[X.columns[index]] = factor

    if not too_high_vif_dict:
        return "No features violate the independence assumption", too_high_vif_dict
    else:
        return "The following features violate the independence assumption", too_high_vif_dict

def calculate_vif_factors(X):
    """
    Runs a variance inflation factor test on each feature, and returns a list
    of the results
    """
    num_features = X.shape[1]
    feature_indices = range(num_features)
    rows = X.values

    return [variance_inflation_factor(rows, i) for i in feature_indices]

def statistically_analyze_homoscedasticity(y, y_hat, X_without_constant):
    """
    Check the homoscedasticity assumption with a statistical test
    Returns a message and a p-value describing the result
    """
    lm_p_value = calculate_breusch_pagan_lagrange_multiplier_p_value(
        y, y_hat, X_without_constant)

    if (lm_p_value < 0.05):
        return "Violates the homoscedasticity assumption according to the Breusch-Pagan test", lm_p_value
    else:
        return "Does not violate the homoscedasticity assumption according to the Breusch-Pagan test", lm_p_value

def calculate_breusch_pagan_lagrange_multiplier_p_value(y, y_hat, X_without_constant):
    """
    Runs a Breusch-Pagan Lagrange Multiplier test for heteroscedasticity
    The null hypothesis is homoscedasticity, alternative hypothesis is
    heteroscedasticity.  Thus returning a low p-value means that the current
    model violates the homoscedasticity assumption
    """
    # for now we discard the statistic and the f-value and it's p-value, just
    # keeping the p-value for the Lagrange Multiplier statistic
    _, lm_p_value, __, ___ = het_breuschpagan(y-y_hat, X_without_constant)
    return lm_p_value

def statistically_analyze_normality(results):
    """
    Check the normality assumption with a statistical test
    Returns a message and a p-value describing the result
    """
    ks_p_value = calculate_kolmogorov_smirnov_statistic_p_value(results)

    if (ks_p_value < 0.05):
        return "Violates the normality assumption according to the Kolmogorov-Smirnov test", ks_p_value
    else:
        return "Does not violate the normality assumption according to the Kolmogorov-Smirnov test", ks_p_value

def calculate_kolmogorov_smirnov_statistic_p_value(results):
    """
    Runs a Kolmogorov-Smirnov test for normality
    The null hypothesis is that the two distributions are identical, alternative
    hypothesis is that they aren't.  Thus returning a low p-value means that the
    current model violates the normality assumption
    """
    # for now we discard the statistic itself, just use the p-value
    _, ks_p_value = kstest(results.resid, 'norm')
    return ks_p_value

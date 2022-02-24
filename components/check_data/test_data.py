import pandas as pd
import numpy as np
import scipy.stats


def test_column_names(data):
    '''
    Check whether column names are supported

    '''

    expected_colums = [
        'customerID',
        'gender',
        'SeniorCitizen',
        'Partner',
        'Dependents',
        'tenure',
        'PhoneService',
        'MultipleLines',
        'InternetService', 
        'OnlineSecurity',
        'OnlineBackup',
        'DeviceProtection',
        'TechSupport',
        'StreamingTV',
        'StreamingMovies',
        'Contract',
        'PaperlessBilling',
        'PaymentMethod',
        'MonthlyCharges',
        'TotalCharges',
        'Churn'
    ]

    these_columns = data.columns.values

    # This also enforces the same order
    assert list(expected_colums) == list(these_columns)


def test_neighborhood_names(data):
    '''
    Test neighbourhood column names.

    '''

    known_names = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

    neigh = set(data['neighbourhood_group'].unique())

    # Unordered check
    assert set(known_names) == set(neigh)


########################################################
# Implement here test_row_count and test_price_range   #
########################################################
def test_row_count(data):
    """
    Test the row count 
    """
    assert 15000 < data.shape[0] < 1000000


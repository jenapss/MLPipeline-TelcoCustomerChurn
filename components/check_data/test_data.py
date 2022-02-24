import pandas as pd
import numpy as np
import scipy.stats


def test_column_names(data):
    '''
    Check whether column names are supported

    '''

    expected_colums = [
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
    
    print(these_columns,'----------')
    print(expected_colums,'1111111')

    # This also enforces the same order
    assert list(expected_colums) == list(these_columns)




########################################################
# Implement here test_row_count and test_price_range   #
########################################################


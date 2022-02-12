import argparse
import logging
import os
import pandas as pd
import wandb
import numpy as np
from wandb_utils.log_artifact import log_artifact
import sklearn

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn import metrics
from sklearn.metrics import roc_curve
from sklearn.metrics import recall_score, confusion_matrix, precision_score, f1_score, accuracy_score, classification_report

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def object_to_int(dataframe_series):
    if dataframe_series.dtype == 'object':
        dataframe_series = LabelEncoder().fit_transform(dataframe_series)
    return dataframe_series


def go(args):
    run = wandb.init(job_type='preprocess_data')
    run.config.update(args)

    logger.info(f'Reading raw data from Weights and Biases')

    artifact_local_path = run.use_artifact(args.input).file()

    df = pd.read_csv(artifact_local_path)
    df = df.drop(['customerID'], axis=1)
    df["TotalCharges"] = pd.to_numeric(df.TotalCharges, errors='coerce')
    df.isnull().sum()
    df[np.isnan(df['TotalCharges'])]

    df[df['tenure'] == 0].index
    df.drop(labels=df[df['tenure'] == 0].index, axis=0, inplace=True)
    df.fillna(df['TotalCharges'].mean())
    df.isnull().sum()
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0: "No", 1: "Yes"})
    # df["InternetService"].describe(include=['object', 'bool'])

    df = df.apply(lambda x: object_to_int(x))

    df.to_csv(
        os.path.join(
            'preprocessed_data',
            'Telco_clean.csv'),
        index=False)
    logger.info(f'Dataset is clean and ready to go now')

    log_artifact(args.output_artifact_name,
                 args.output_artifact_type,
                 args.output_description,
                 os.path.join('preprocessed_data', 'Telco_clean.csv'),
                 run,)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Download URL to local destination")
    # parser.add_argument('sample', type=str, help='Name of sample to download')
    parser.add_argument('input', type=str, help='Name for the input artifact')
    parser.add_argument(
        'output_artifact_name',
        type=str,
        help='Name for the output artifact')
    parser.add_argument(
        'output_artifact_type',
        type=str,
        help='Type of output artifact')
    parser.add_argument(
        'output_description',
        type=str,
        help='Description of this artifact')

    args = parser.parse_args()

    go(args)

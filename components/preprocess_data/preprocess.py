import argparse
import logging
import os
import pandas as pd
import wandb

from wandb_utils.log_artifact import log_artifact


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def object_to_int(dataframe_series):
    if dataframe_series.dtype=='object':
        dataframe_series = LabelEncoder().fit_transform(dataframe_series)
    return dataframe_series



def go(args):
    run = wandb.init(job_type='download_file')
    run.config.update(args)

    logger.info(f"Returning sample {args.sample}")
    logger.info(f'Uploading {args.artifact_name} to Weights and Biases')

    df = pd.read_csv(os.path.join('data', 'Telco1.csv'))
    df = df.drop(['customerID'], axis = 1)
    df["TotalCharges"] = pd.to_numeric(df.TotalCharges, errors = 'coerce')
    df.isnull().sum()
    df[np.isnan(df['TotalCharges'])]

    df[df['tenure']==0].index

    df.fillna(df['TotalCharges'].mean())
    df.isnull().sum()
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0: "No", 1: "Yes"})
    df["InternetService"].describe(include=['object', 'bool'])

    df = df.apply(lambda x: object_to_int(x))

    df.to_csv(os.path.join('preprocessed_data', 'Telco_clean.csv'), index= False)
    logger.info(f'Dataset is clean and ready to go now')


    log_artifact(args.artifact_name,
                 args.artifact_type,
                 args.artifact_description,
                 os.path.join('preprocessed_data', args.sample),
                 run,)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download URL to local destination")
    parser.add_argument('sample', type=str, help='Name of sample to download')
    parser.add_argument('artifact_name', type=str, help='Name for the output artifact')
    parser.add_argument('artifact_type', type=str, help='Type of output artifact')
    parser.add_argument('artifact_description', type=str, help='Description of this artifact')

    args.parser.parser_args()

    go(args)
    
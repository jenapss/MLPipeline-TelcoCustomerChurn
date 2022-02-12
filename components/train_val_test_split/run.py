import argparse
import logging
import pandas as pd
import wandb
import tempfile
from sklearn.model_selection import train_test_split
from wandb_utils.log_artifact import log_artifact

import tempfile
import numpy as np
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s')
logger = logging.getLogger()

def go(args):
    run = wandb.init(job_type='train_test_split')
    run.config.update(args)
    logger.info(f'Fetching artifact {args.input}')


    artifact_local_path = run.use_artifact(args.input).file()
    df = pd.read_csv(artifact_local_path)

    logger.info("Splitting trainval and test")

    X = df.drop(columns = ['Churn'])
    y = df['Churn'].values



    X_train, X_test, y_train, y_test = train_test_split(
        X,y,
        test_size = args.test_size,
        random_state = args.random_seed,
        stratify = y
    )

    
    
    for df, k in zip([X_train, X_test], ['X_train', 'X_test']):
        logger.info(f'Uploading {k}_data.csv dataset')
        with tempfile.NamedTemporaryFile('w') as fp:

            df.to_csv(fp.name, index=False)

            log_artifact(
                f'{k}_data.csv',
                f'{k}_data',
                f'{k} split of dataset',
                fp.name, run
            )

    with tempfile.NamedTemporaryFile('w') as fp:
        np.save('y_train.npy', y_train)
        log_artifact(
            'y_train.npy',
            'y_train',
            'y_train split of dataset',
            'y_train.npy', run
        )
    with tempfile.NamedTemporaryFile('w') as fp:
        np.save('y_test.npy', y_test)
        log_artifact(
            'y_test.npy',
            'y_test',
            'y_test split of dataset',
            'y_test.npy', run
        )
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split test and remainder")

    parser.add_argument("input", type=str, help="Input artifact to split")

    parser.add_argument(
        "test_size", type=float, help="Size of the test split. Fraction of the dataset, or number of items"
    )

    parser.add_argument(
        "--random_seed", type=int, help="Seed for random number generator", default=42, required=False
    )


    args = parser.parse_args()

    go(args)

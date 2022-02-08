import argparse
import logging
import pandas as pd
import wandb
import tempfile
from sklearn.model_selection import train_test_split
from wandb_utils.log_artifact import log_artifact

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s')
logger = logging.getLogger()

def go(args):
    run = wandb.init(job_type='train_test_split')
    run.config.update(args)

    logger.info(f'Fetching artifact {args.input}')
    artifact_local_path = run.use_artifact(args.input).file()

    df = pd.read_csv(artifact_local_path)

    logger.info("Splitting trainval and test")

    trainval, test = train_test_split(
        df,
        test_size=args.test_size,
        random_state=args.random_seed,
        stratify = df[args.stratify_by] if args.stratify_by != 'none' else None,
    )

    for df, k in zip([trainval, test], ['trainval', 'test']):
        logger.info(f'Uploading {k}_data.csv dataset')
        with teamfile.NamedTemporaryFile('w') as fp:

            df.to_csv(fp.name, index=False)

            log_artifact(
                f'{k}_data.csv',
                f'{k}_data',
                f'{k} split of dataset',
                fp.name, run
            )
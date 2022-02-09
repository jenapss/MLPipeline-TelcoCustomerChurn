import argparse
import logging
import os
import wandb
from wandb_utils.log_artifact import log_artifact


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(job_type='download_file')
    run.config.update(args)

    logger.info(f"Returning sample {args.sample}")
    logger.info(f'Uploading {args.artifact_name} to Weights and Biases')

    log_artifact(args.artifact_name,
                 args.artifact_type,
                 args.artifact_description,
                 os.path.join('data', args.sample),
                 run,)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download URL to local destination")
    parser.add_argument('sample', type=str, help='Name of sample to download')
    parser.add_argument('artifact_name', type=str, help='Name for the output artifact')
    parser.add_argument('artifact_type', type=str, help='Type of output artifact')
    parser.add_argument('artifact_description', type=str, help='Description of this artifact')

    args.parser.parser_args()

    go(args)
    
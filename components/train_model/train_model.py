import argparse
import logging
import os
import wandb
from sklearn.model_selection import train_test_split
from wandb_utils.log_artifact import log_artifact
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
from sklearn import metrics
from sklearn.metrics import roc_curve
from sklearn.metrics import recall_score, confusion_matrix, precision_score, f1_score, accuracy_score, classification_report
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="train_random_forest")
    run.config.update(args)

    logger.info(f'Reading preprocessed data from Weights and Biases')

    training_artifact = run.use_artifact(args.train_data).file()

    training_data = pd.read_csv(training_artifact,encoding="ISO-8859–1")

    # print(type(training_data))

    X = training_data.drop(columns = ['Churn'])
    y = training_data['Churn'].values

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.30, random_state = 40, stratify=y)

    logger.info("Preparing sklearn pipeline")

    scaler= StandardScaler()

    num_cols = ["tenure", 'MonthlyCharges', 'TotalCharges']

    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    model_rf = RandomForestClassifier(n_estimators=500 , oob_score = True, n_jobs = -1,
                                  random_state =50, max_features = "auto",
                                  max_leaf_nodes = 30)
    model_rf.fit(X_train, y_train)

    # Make predictions
    prediction_test = model_rf.predict(X_test)
    print(metrics.accuracy_score(y_test, prediction_test))
    joblib.dump(model_rf, "/Users/jelaleddin/MLPipeline-TelcoCustomerChurn/components/train_model/model/my_random_forest.joblib")
    logger.info("Random Forest Model saved")
    
    log_artifact("Random_Forest_model",
                 'joblib model file',
                 'trained random forest model',
                 os.path.join('model', 'my_random_forest.joblib'),
                 run,)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Train Random Forest Model")
    # parser.add_argument('sample', type=str, help='Name of sample to download')
    parser.add_argument('train_data', type=str, help='Name for the input training artifact')

    args = parser.parse_args()

    go(args)
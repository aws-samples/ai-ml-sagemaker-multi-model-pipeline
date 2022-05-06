# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Evaluation script for measuring model accuracy."""

import json
import logging
import os
import pickle
import tarfile

import pandas as pd
import numpy
#import xgboost
#import boto3

#from os import listdir


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# May need to import additional metrics depending on what you are measuring.
# See https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality-metrics.html
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, mean_squared_error, mean_absolute_error, r2_score

if __name__ == "__main__":
    logger.info("START MAIN")
    tar_model_path = "/opt/ml/processing/model/model.tar.gz"
    model_path = "/opt/ml/processing/model/decision-tree-model.pkl"
    
    with tarfile.open(tar_model_path) as tar:
        tar.extractall(path="/opt/ml/processing/model/")
 
    #logger.info(os.listdir("/opt/ml/processing/model/"))
    #logger.info(os.listdir("/opt/ml/processing/"))
    #logger.info(os.system("pwd"))
    #logger.info(os.listdir("/opt/program/"))
    #logger.info(os.listdir("/opt/"))
    
        
    logger.debug("Loading DTree model.")
    #with open(model_path, "rb") as inp:
    #    model = pickle.load(inp)
        
    model = pickle.load(open(model_path, "rb"))
    
    
   # model = pickle.load(open("xgboost-model", "rb"))


    test_path = "/opt/ml/processing/test/test.csv"
    
    
    print("Loading test input data")
    
    
    df = pd.read_csv(test_path, header=None)
    
    logger.debug("Reading test data.")
    y_test = df.iloc[:, 0].to_numpy()
    df.drop(df.columns[0], axis=1, inplace=True)
    X_test = numpy.array(df.values)
    logger.info(X_test[0])
    
    
    #predictions = []
    #for array in numpy.array_split(X_test, 100):
    #    pred_response = ll_predictor.predict(array, initial_args={"ContentType": "text/csv"})
    #    predictions += [r["score"] for r in pred_response["predictions"]]
    #    logger.info(predictions)



    #logger.debug("Reading test data.")
    #y_test = df.iloc[:, 0].to_numpy()

    #df.drop(df.columns[0], axis=1, inplace=True)
    #X_test = xgboost.DMatrix(df.values)
 
    

    logger.info("Performing predictions against test data.")
    predictions = model.predict(X_test)
    
    

    print("Creating classification evaluation report")
    #acc = accuracy_score(y_test, predictions.round())
    #auc = roc_auc_score(y_test, predictions.round())
    
    
    mse = mean_squared_error(y_test, predictions)
    r2s = r2_score(y_test, predictions)


    report_dict = {
        "regression_metrics": {
            "mse": {"value": mse},
            "r2s": {"value": r2s},
        },
    }

    print("Classification report:\n{}".format(report_dict))

    evaluation_output_path = os.path.join("/opt/ml/processing/evaluation", "dtree_evaluation.json")
    print("Saving classification report to {}".format(evaluation_output_path))

    with open(evaluation_output_path, "w") as f:
        f.write(json.dumps(report_dict))
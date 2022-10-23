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

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# May need to import additional metrics depending on what you are measuring.
# See https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality-metrics.html
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

if __name__ == "__main__":

    prefix = "/opt/ml/processing/"
    tar_model_path = os.path.join(prefix, 'model/model.tar.gz')
    model_path = os.path.join(prefix, 'model/decision-tree-model.pkl')
    
    os.system('sudo chown -R 1000:100 ' + prefix)
    with tarfile.open(tar_model_path) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path="/opt/ml/processing/model/")

    logger.debug("Loading DTree model.")

    model = pickle.load(open(model_path, "rb"))

    test_path = "/opt/ml/processing/test/test.csv"

    logger.info("Loading test input data")

    df = pd.read_csv(test_path, header=None)
   
    logger.debug("Reading test data.")
    y_test = df.iloc[:, 0].to_numpy()
    df.drop(df.columns[0], axis=1, inplace=True)
    X_test = numpy.array(df.values)

    logger.info("Performing predictions against test data.")
    predictions = model.predict(X_test)

    logger.info("Creating classification evaluation report")

    acc = accuracy_score(y_test, predictions)
    roc = roc_auc_score(y_test, predictions)

    report_dict = {
        "classification_metrics": {
            "acc": {"value": acc},
            "roc": {"value": roc},
        },
    }

    logger.info("Regression report:\n{}".format(report_dict))

    evaluation_output_path = os.path.join("/opt/ml/processing/evaluation", "dtree_evaluation.json")
    logger.info("Saving regression report to {}".format(evaluation_output_path))

    with open(evaluation_output_path, "w") as f:
        f.write(json.dumps(report_dict))

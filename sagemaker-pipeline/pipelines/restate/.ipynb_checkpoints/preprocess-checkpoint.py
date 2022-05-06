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
"""Feature engineers the customer churn dataset."""
import argparse
import logging
import pathlib

import boto3
import numpy as np
import pandas as pd

import os
import glob

#import awswrangler as wr

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    logger.info("Starting preprocessing.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str, required=True)
    #parser.add_argument("--input-data-wr", type=str, required=True)
    args = parser.parse_args()
    logger.info("setting memory workaround")
    os.system("echo 1 > /proc/sys/vm/overcommit_memory")
    logger.info("done memory workaround")
    base_dir = "/opt/ml/processing"
    pathlib.Path(f"{base_dir}/data").mkdir(parents=True, exist_ok=True)
    input_data = args.input_data
    print(input_data)
    bucket = input_data.split("/")[2]
    s3_output_prefix = "/".join(input_data.split("/")[3:])

    
    s3_resource = boto3.resource('s3') 
    temp_s3_bucket = s3_resource.Bucket(bucket)
    prefix_objs = temp_s3_bucket.objects.filter(Prefix=s3_output_prefix)
    logger.info("s3_output_prefix is: %s", s3_output_prefix)
    for obj in prefix_objs:
        key = obj.key
        logger.info(key)
        logger.info("Downloading data from bucket: %s, key: %s", bucket, key)
        s3fn = key.split("/")
        s3fn = s3fn[len(s3fn)-1]
        fn = f"{base_dir}/data/{s3fn}"
        s3_resource.Bucket(bucket).download_file(key, fn)
        

    logger.info("Reading downloaded data.")
    all_files = glob.iglob(os.path.join(f"{base_dir}/data", "*.csv")) 
    df_from_each_file = (pd.read_csv(f) for f in all_files)
    model_data = pd.concat(df_from_each_file, ignore_index=True)

    # read in csv
    #model_data = pd.read_csv(fn)
    logger.info(model_data.info())
    logger.info(len(model_data))
    logger.info(len(model_data.columns))
    
    # data wrangler is not installed!
    #model_data = wr.s3.read_csv(input_data_wr, chunksize=1000)

    # drop the "Phone" feature column
    #df = df.drop(["Phone"], axis=1)

    # Change the data type of "Area Code"
    #df["Area Code"] = df["Area Code"].astype(object)

    # Drop several other columns
    #df = df.drop(["Day Charge", "Eve Charge", "Night Charge", "Intl Charge"], axis=1)

    # Convert categorical variables into dummy/indicator variables.
    #model_data = pd.get_dummies(df)

    # Create one binary classification target column
    #model_data = pd.concat(
    #    [
    #        model_data["Churn?_True."],
    #        model_data.drop(["Churn?_False.", "Churn?_True."], axis=1),
    #    ],
    #    axis=1,
    #)
    print("1 - Showing first rows..")
    print(model_data.loc[[0]])
    print(model_data.loc[[1]])
    print(model_data.loc[[2]])
    
    
    # Split the data
    train_data, validation_data, test_data = np.split(
        model_data.sample(frac=1, random_state=1729),
        [int(0.7 * len(model_data)), int(0.9 * len(model_data))],
    )

    logger.info("TRAIN DATA INFO")
    logger.info(train_data.info())
    logger.info(len(train_data))
    logger.info(len(train_data.columns))
    logger.info("TEST DATA INFO")
    logger.info(test_data.info())
    logger.info(len(test_data))
    logger.info(len(test_data.columns))  
    logger.info("VALIDATION DATA INFO")
    logger.info(validation_data.info())
    logger.info(len(validation_data))
    logger.info(len(validation_data.columns))  
    
    test_data = test_data[train_data.columns]
    validation_data = validation_data[train_data.columns]
          
    pd.DataFrame(train_data).to_csv(f"{base_dir}/train/train.csv", header=False, index=False)
    pd.DataFrame(validation_data).to_csv(
        f"{base_dir}/validation/validation.csv", header=False, index=False
    )
    pd.DataFrame(test_data).to_csv(f"{base_dir}/test/test.csv", header=False, index=False)
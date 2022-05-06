## Layout of the Multi-model SageMaker Pipeline with Hyperparamater Tuning and Experiments Template

This project has two (2) components: (1) container - custom Docker image with custom Decision Tree  algorithm using scikit-learn with hyperpameter tuning support, and (2) sagemaker-pipeline - a SageMaker pipeline that supports two (2) algorithms: XGBoost on SageMaker container and Decision Tree on custom container built from the first component. The pipeline imports the data from an Athena table and is transformed for ML training using SageMaker Data Wrangler. The pipeline also supports SageMaker HyperParameter Tuning and SageMaker Experiments. The best performing model in terms of R2 Score is then registered to the model registry, ready for inference deployment.


```
|-- CONTRIBUTING.md
|-- README.md
|-- XXXnotebook
|-- sagemaker-pipeline
|   |-- codebuild-buildspec.yml
|   |-- pipelines
|   |   |-- restate
|   |   |   |-- xgb_evaluate.py
|   |   |   |-- dtree_evaluate.py
|   |   |   |-- __init__.py
|   |   |   |-- pipeline.py
|   |   |   `-- preprocess.py
|   |   |-- get_pipeline_definition.py
|   |   |-- __init__.py
|   |   |-- run_pipeline.py
|   |   |-- _utils.py
|   |   `-- __version__.py
|   |-- setup.cfg
|   |-- setup.py
|   |-- tests
|   |   `-- test_pipelines.py
|   `-- tox.ini
|-- container
|   |-- XXX
```

## Start here

In this example, we are solving real estate value regression prediction problem using the Russia Real Estate 2018-2021 dataset. The dataset is imported to an Athena table from S3 and the pipeline imports the data from this table. Data Wrangler transforms the data (i.e. one-hot encoding, etc) as the initial step in the pipeline. The pipeline then proceeds with preprocessing, training using Decision Tree and XGBoost algorithms with hyperparameter tuning, evaluation, and registration of the winning model to the registry. Every trial is recorded in SageMaker Experiments. This pipeline is a modified version of [SageMaker Secure MLOps](https://github.com/aws-samples/amazon-sagemaker-secure-mlops/tree/master/mlops-seed-code/model-build-train).

Prior to running the pipeline, you have to push the Decision Tree custom container to your own Amazon Elastic Container Registry (ECR). This container is a modified version of [Scikit BYO](https://github.com/aws/amazon-sagemaker-examples/tree/main/advanced_functionality/scikit_bring_your_own/container).

You can  use the `restate-project.ipynb` notebook to experiment from SageMaker Studio before you are ready to checkin your code.

## Dataset

The dataset used is the [Russia Real Estate 2018-2021] (https://www.kaggle.com/datasets/mrdaniilak/russia-real-estate-20182021).

The dataset contains the following features:
    date - date of publication of the announcement
    region - region of Russia, there are 85 subjects in the country in total
    building_type - facade type. 0 - Other. 1 - Panel. 2 - Monolithic. 3 - Brick. 4 - Blocky. 5 - Wooden
    object_type - apartment type. 1 - Secondary real estate market; 2 - New building
    levels - number of floors
    rooms - the number of living rooms, if the value is "-1", then it means "studio apartment"
    area - the total area of ​​the apartment
    kitchen_area - kitchen area
    price - price in Rubles


## Assumptions and Prerequisites

    1. S3 bucket sagemaker-restate-<AWS ACCOUNT ID> is created and raw data has been uploaded to s3://sagemaker-restate-<AWS ACCOUNT ID>/raw/russia/.
    2. SageMaker project is already created.
    3. Necessary IAM service roles are already created.


## Security

This sample code is not designed for production deployment out-of-the-box, so further security enhancements may need to be added according to your own requirements before pushing to production. Security recommendations include, but are not limited to, the following:
- Use private ECR
- Use a more defined IAM permission for service roles
- Use S3 VPC endpoint policy which controls access to specified Amazon S3 buckets only
- Use interface VPC endpoints to prevent communication traffic from traversing  public network

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

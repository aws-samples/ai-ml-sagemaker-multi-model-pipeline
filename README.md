# Predict diabetic patient readmission using multi-model training on SageMaker Pipelines

This project has two (2) components: (1) `container` - custom Docker image with custom Decision Tree  algorithm using scikit-learn with hyperpameter tuning support, and (2) `sagemaker-pipeline` - a SageMaker pipeline that supports two (2) algorithms: XGBoost on SageMaker container and Decision Tree on custom container built from the first component. The pipeline imports the data from an S3 bucket for ML training using SageMaker Data Wrangler. The pipeline also supports SageMaker HyperParameter Tuning. The best performing model in terms of RPC is then registered to the model registry, ready for inference deployment.

## Start here

In this example, we are solving binary classification problem to determine if a hospital diabetic patient is predicted to be readmitted in the hospital. This example uses [Diabetes 130-US hospitals for years 1999-2008 Data Set](https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008). The dataset is uploaded to an S3 bucket and the pipeline imports the data from this bucket. Data Wrangler transforms the data (i.e. one-hot encoding, etc) as the initial step in the pipeline. The pipeline then proceeds with preprocessing, training using Decision Tree and XGBoost algorithms with hyperparameter tuning, evaluation, and registration of the winning model to the registry. This pipeline is a modified version of the pipeline provided by [Amazon SageMaker Examples multi-model pipeline](https://github.com/aws/amazon-sagemaker-examples/tree/main/sagemaker-pipeline-multi-model).

Prior to running the pipeline, you have to push the Decision Tree custom container to your own Amazon Elastic Container Registry (ECR). This container is a modified version of [Scikit BYO](https://github.com/aws/amazon-sagemaker-examples/tree/main/advanced_functionality/scikit_bring_your_own/container).

You can use the `diabetes-project.ipynb` notebook to experiment from SageMaker Studio before you are ready to checkin your code.

## DataSet

The dataset represents 10 years (1999-2008) of clinical care at 130 US hospitals and integrated delivery networks. It includes over 50 features representing patient and hospital outcomes. Information was extracted from the database for encounters that satisfied the following criteria. More dataset information can be found in [Diabetes 130-US hospitals for years 1999-2008 Data Set](https://archive.ics.uci.edu/ml/datasets/diabetes+130-us+hospitals+for+years+1999-2008).

## Assumptions and Prerequisites

- S3 bucket `sagemaker-diabetes-<AWS ACCOUNT ID>` is created and raw data has been uploaded to `s3://sagemaker-diabetes-<AWS ACCOUNT ID>/`.
- SageMaker project is already created. Recommendation is to create a SageMaker project using [SageMaker-provide MLOps template for model building, training, and deployment template](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-templates-sm.html#sagemaker-projects-templates-code-commit).
- Necessary IAM service roles are already created.

## Security

This sample code is not designed for production deployment out-of-the-box, so further security enhancements may need to be added according to your own requirements before pushing to production. Security recommendations include, but are not limited to, the following:
- Use private ECR
- Use a more defined IAM permission for service roles
- Use interface / gateway VPC endpoints to prevent communication traffic from traversing public network
- Use S3 VPC endpoint policy which controls access to specified Amazon S3 buckets only

AmazonSageMakerServiceCatalogProductsUseRole-diabetes with AmazonSageMakerFullAccess. [This is required as we are creating a custom SageMaker image](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-byoi-create.html).


[diabetes-project.ipynb](diabetes-project.ipynb) has been tested in a SageMaker notebook instance that is using a kernel with Python 3.7 installed. This SageMaker notebook is attached with an [IAM role with an in-line policy](diabetes-project-iam.json).

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

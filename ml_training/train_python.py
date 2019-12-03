from time import sleep

from sagemaker.amazon.amazon_estimator import get_image_uri
from sagemaker.predictor import csv_serializer
import sagemaker_role
import pandas as pd
import boto3
import os
import sagemaker
import numpy as np


def main():

    train = pd.read_csv('./fall_train.csv', names=list(range(37)), index_col=False)
    test = pd.read_csv('./fall_test.csv', names=list(range(37)), index_col=False)


    #
    # Training and Validation Set
    #
    #     Target Variable as first column followed by input features
    #     raining, Validation files do not have a column header
    #
    #

    train_labels = np.array(train.iloc[:, 0]).astype("int")
    test_labels = np.array(test.iloc[:, 0]).astype("int")

    train_features = np.array(train.iloc[:, 1:]).astype("float32")
    test_features = np.array(test.iloc[:, 1:]).astype("float32")

    # Upload Data to S3
    #TODO
    bucket_name = 'sagemaker-eu-central-1-19111535'
    training_file_key = 'model_data/fall_train.csv'
    validation_file_key = 'model_data/fall_validation.csv'
    test_file_key = 'model_data/fall_test.csv'

    s3_model_output_location = r's3://{0}/model_data/model'.format(bucket_name)
    s3_training_file_location = r's3://{0}/{1}'.format(bucket_name, training_file_key)
    s3_validation_file_location = r's3://{0}/{1}'.format(bucket_name, validation_file_key)
    s3_test_file_location = r's3://{0}/{1}'.format(bucket_name, test_file_key)


    print(s3_model_output_location)
    print(s3_training_file_location)
    print(s3_validation_file_location)
    print(s3_test_file_location)


    # Write and Reading from S3 is just as easy
    # files are referred as objects in S3.
    # file name is referred as key name in S3
    # Files stored in S3 are automatically replicated across 3 different availability zones
    # in the region where the bucket was created.

    # http://boto3.readthedocs.io/en/latest/guide/s3.html
    def write_to_s3(filename, bucket, key):
        with open(filename, 'rb') as f:  # Read in binary mode
            return boto3.Session().resource('s3').Bucket(bucket).Object(key).upload_fileobj(f)


    write_to_s3('fall_train.csv', bucket_name, training_file_key)
    write_to_s3('fall_validation.csv', bucket_name, validation_file_key)
    write_to_s3('fall_test.csv', bucket_name, test_file_key)


    #
    # Training Algorithm Docker Image
    #
    #     AWS Maintains a separate image for every region and algorithm
    #

    role = sagemaker_role.create_role_sagemaker()
    # chiamata di creazione del ruolo e' asincrona
    sleep(20)

    # Build Model
    sess = sagemaker.Session()

    # Access appropriate algorithm container image
    #  Specify how many instances to use for distributed training and what type of machine to use
    #  Finally, specify where the trained model artifacts needs to be stored
    #   Reference: http://sagemaker.readthedocs.io/en/latest/estimators.html
    #    Optionally, give a name to the training job using base_job_name
    container_path = get_image_uri(boto3.Session().region_name, 'xgboost', repo_version='0.90-1')

    estimator = sagemaker.estimator.Estimator(container_path,
                                              role,
                                              train_instance_count=1,
                                              train_instance_type='ml.m5.large',
                                              output_path=s3_model_output_location,
                                              sagemaker_session=sess,
                                              base_job_name='xgboost-fall-v1')


    # In[12]:


    # Specify hyper parameters that appropriate for the training algorithm
    # XGBoost Training Parameter Reference:
    #   https://github.com/dmlc/xgboost/blob/master/doc/parameter.md

    # max_depth=5,eta=0.1,subsample=0.7,num_round=150
    estimator.set_hyperparameters(max_depth=6, objective="reg:linear",
                                  eta=0.12, subsample=0.73, num_round=200)


    estimator.hyperparameters()


    # Specify Training Data Location and Optionally, Validation Data Location


    # content type can be libsvm or csv for XGBoost
    training_input_config = sagemaker.session.s3_input(s3_data=s3_training_file_location, content_type="csv")
    validation_input_config = sagemaker.session.s3_input(s3_data=s3_validation_file_location, content_type="csv")

    print(training_input_config.config)
    print(validation_input_config.config)


    # Train the model

    # XGBoost supports "train", "validation" channels
    # Reference: Supported channels by algorithm
    #   https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-algo-docker-registry-paths.html
    estimator.fit({'train': training_input_config, 'validation': validation_input_config})




if __name__ == '__main__':
    main()
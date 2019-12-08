from time import sleep

from sagemaker.amazon.amazon_estimator import get_image_uri
from sagemaker.predictor import csv_serializer
import sagemaker_role
import sys

import boto3
import sagemaker


def write_to_s3(filename, bucket, key):
    with open(filename, 'rb') as f:  # Read in binary mode
        return boto3.Session().resource('s3').Bucket(bucket).Object(key).upload_fileobj(f)


def upload_data(bucket_name):
    # Upload Data to S3

    # posizione dati in s3
    training_file_key = 'model_data/fall_train.csv'
    test_file_key = 'model_data/fall_test.csv'

    s3_model_output_location = r's3://{0}/model_data/model'.format(bucket_name)
    s3_training_file_location = r's3://{0}/{1}'.format(bucket_name, training_file_key)

    write_to_s3('fall_train.csv', bucket_name, training_file_key)
    write_to_s3('fall_test.csv', bucket_name, test_file_key)

    return s3_model_output_location, s3_training_file_location


def create_endpoint(estimator):
    # genera un endpoint per il modello
    # Ref: http://sagemaker.readthedocs.io/en/latest/estimators.html
    predictor = estimator.deploy(initial_instance_count=1,
                                 instance_type='ml.m5.large',  # 'ml.m5.4xlarge',
                                 endpoint_name='xgboost-fall-v1')

    predictor.content_type = 'text/csv'
    predictor.serializer = csv_serializer
    predictor.deserializer = None

    return predictor


def evaluate_model(predictor, test_features, test_labels):
    # calcola gli errori del modello
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for i in range(1, len(test_features)):
        pred = predictor.predict([test_features[i]])
        pred = round(float(pred))

        if pred == 0 and test_labels[i] == 0:
            true_negative = true_negative + 1
        if pred == 0 and test_labels[i] == 1:
            false_negative = false_negative + 1
        if pred == 1 and test_labels[i] == 1:
            true_positive = true_positive + 1
        if pred == 1 and test_labels[i] == 0:
            false_positive = false_positive + 1

    print(true_positive)  # 48
    print(true_negative)  # 137
    print(false_positive)  # 0
    print(false_negative)  # 1


def delete_endpoint():
    client = boto3.client('sagemaker')
    client.delete_endpoint(EndpointName='xgboost-fall-v1')


def train_model(s3_model_output_location, s3_training_file_location):

    # crea i ruoli necessari per la creazione di endpoint e per l'uso di sagemaker
    role = sagemaker_role.create_role_sagemaker()

    # chiamata di creazione del ruolo e' asincrona
    sleep(20)

    # Build Model
    sess = sagemaker.Session()

    # Access appropriate algorithm container image
    #  Specify how many instances to use for distributed training and what type of machine to use
    #  Finally, specify where the trained model artifacts needs to be stored
    #   Reference: http://sagemaker.readthedocs.io/en/latest/estimators.html
    container_path = get_image_uri(boto3.Session().region_name, 'xgboost', repo_version='0.90-1')

    estimator = sagemaker.estimator.Estimator(container_path,
                                              role,
                                              train_instance_count=1,
                                              train_instance_type='ml.m5.large',
                                              output_path=s3_model_output_location,
                                              sagemaker_session=sess,
                                              base_job_name='xgboost-fall-v1')

    # Specify hyper parameters that appropriate for the training algorithm
    # XGBoost Training Parameter Reference:
    #   https://github.com/dmlc/xgboost/blob/master/doc/parameter.md

    # max_depth=5,eta=0.1,subsample=0.7,num_round=150
    estimator.set_hyperparameters(max_depth=6, objective="reg:linear",
                                  eta=0.12, subsample=0.73, num_round=200)

    estimator.hyperparameters()

    # content type can be libsvm or csv for XGBoost
    training_input_config = sagemaker.session.s3_input(s3_data=s3_training_file_location, content_type="csv")

    estimator.fit({'train': training_input_config})

    return estimator


def main():

    if len(sys.argv) < 2:
        print("Usage: python3 train_python.py <name of bucket>")
        exit()

    bucket_name = sys.argv[1]
    s3_model_output_location, s3_training_file_location = upload_data(bucket_name)

    estimator = train_model(s3_model_output_location, s3_training_file_location)

    # optionaly
    # predictor = create_endpoint(estimator)
    #
    # test = pd.read_csv('./fall_test.csv', names=list(range(37)), index_col=False)
    # test_labels = np.array(test.iloc[:, 0]).astype("int")
    # test_features = np.array(test.iloc[:, 1:]).astype("float32")
    #
    # evaluate_model(predictor, test_features, test_labels)
    # delete_endpoint()


# 'sagemaker-eu-central-1-19111535'
if __name__ == '__main__':
    main()

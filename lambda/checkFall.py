import os
import boto3
import json
from io import StringIO
from scipy.stats import kurtosis, skew
import pandas as pd
import numpy as np

# grab environment variables
# ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')
ENDPOINT_NAME = 'fall-model-endpoint'

max_acc = 8
min_acc = -8
max_gir = 300
min_gir = -300
x_acc_mean = -0.2253104
y_acc_mean = -0.001440401
z_acc_mean = 0.2755269
x_gir_mean = -3.499445
y_gir_mean = 0.2408492
z_gir_mean = -1.55567


def handler(event, context):
    for record in event['Records']:
        attributes = record["Sns"]["MessageAttributes"]
        sensor_id = attributes["sensor_id"]["Value"]
        timestamp = attributes["timestamp"]["Value"]
        latitude = attributes["latitude"]["Value"]
        longitude = attributes["longitude"]["Value"]
        heart_rate = attributes["heart_rate"]["Value"]
        fall_data = attributes["fall_data"]["Value"]

        data_vector = read_message(fall_data)

        df_acc_x = remove_outlier_and_fix_missing(data_vector[0], max_acc, min_acc)
        df_acc_y = remove_outlier_and_fix_missing(data_vector[1], max_acc, min_acc)
        df_acc_z = remove_outlier_and_fix_missing(data_vector[2], max_acc, min_acc)

        df_gir_x = remove_outlier_and_fix_missing(data_vector[3], max_gir, min_gir)
        df_gir_y = remove_outlier_and_fix_missing(data_vector[4], max_gir, min_gir)
        df_gir_z = remove_outlier_and_fix_missing(data_vector[5], max_gir, min_gir)

        # normalizzazione dei dati
        df_acc_x = ((df_acc_x - x_acc_mean) / (max_acc - min_acc))
        df_acc_y = ((df_acc_y - y_acc_mean) / (max_acc - min_acc))
        df_acc_z = ((df_acc_z - z_acc_mean) / (max_acc - min_acc))

        df_gir_x = ((df_gir_x - x_gir_mean) / (max_gir - min_gir))
        df_gir_y = ((df_gir_y - y_gir_mean) / (max_gir - min_gir))
        df_gir_z = ((df_gir_z - z_gir_mean) / (max_gir - min_gir))

        x_acc_str = "{:.9f}".format(max(df_acc_x)) + ',' + "{:.9f}".format(min(df_acc_x)) + ',' + "{:.9f}".format(
            np.mean(df_acc_x)) + ',' + "{:.9f}".format(np.var(df_acc_x)) + ',' + "{:.9f}".format(
            kurtosis(df_acc_x)) + ',' + "{:.9f}".format(skew(df_acc_x))
        x_gir_str = "{:.9f}".format(max(df_gir_x)) + ',' + "{:.9f}".format(min(df_gir_x)) + ',' + "{:.9f}".format(
            np.mean(df_gir_x)) + ',' + "{:.9f}".format(np.var(df_gir_x)) + ',' + "{:.9f}".format(
            kurtosis(df_gir_x)) + ',' + "{:.9f}".format(skew(df_gir_x))

        y_acc_str = "{:.9f}".format(max(df_acc_y)) + ',' + "{:.9f}".format(min(df_acc_y)) + ',' + "{:.9f}".format(
            np.mean(df_acc_y)) + ',' + "{:.9f}".format(np.var(df_acc_y)) + ',' + "{:.9f}".format(
            kurtosis(df_acc_y)) + ',' + "{:.9f}".format(skew(df_acc_y))
        y_gir_str = "{:.9f}".format(max(df_gir_y)) + ',' + "{:.9f}".format(min(df_gir_y)) + ',' + "{:.9f}".format(
            np.mean(df_gir_y)) + ',' + "{:.9f}".format(np.var(df_gir_y)) + ',' + "{:.9f}".format(
            kurtosis(df_gir_y)) + ',' + "{:.9f}".format(skew(df_gir_y))

        z_acc_str = "{:.9f}".format(max(df_acc_z)) + ',' + "{:.9f}".format(min(df_acc_z)) + ',' + "{:.9f}".format(
            np.mean(df_acc_z)) + ',' + "{:.9f}".format(np.var(df_acc_z)) + ',' + "{:.9f}".format(
            kurtosis(df_acc_z)) + ',' + "{:.9f}".format(skew(df_acc_z))
        z_gir_str = "{:.9f}".format(max(df_gir_z)) + ',' + "{:.9f}".format(min(df_gir_z)) + ',' + "{:.9f}".format(
            np.mean(df_gir_z)) + ',' + "{:.9f}".format(np.var(df_gir_z)) + ',' + "{:.9f}".format(
            kurtosis(df_gir_z)) + ',' + "{:.9f}".format(skew(df_gir_z))

        payload = x_acc_str + ',' + y_acc_str + ',' + z_acc_str + ',' + x_gir_str + ',' + y_gir_str + ',' + z_gir_str
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                           ContentType='text/csv',
                                           Body=payload)

        # print(response)
        result = json.loads(response['Body'].read().decode())
        # print(result)

        result = round(float(result))
        #print(result)

        if result == 0:
            print("JOB_ID {}, RequestId: {}"
                  .format(sensor_id + timestamp.replace('.', '-'), context.aws_request_id))
        else:
            # Create an SNS client
            sns = boto3.client('sns')

            # Publish a simple message to the specified SNS topic
            response = sns.publish(
                TopicArn=os.environ['SNS_TOPIC_NOTIFY'],
                Message='Attenzione: caduta rilevata',
                MessageAttributes={
                    'sensor_id': {
                        'DataType': 'Number',
                        'StringValue': sensor_id
                    },
                    'timestamp': {
                        'DataType': 'String',
                        'StringValue': timestamp
                    },
                    'type': {
                        'DataType': 'String',
                        'StringValue': 'Caduta'
                    },
                    'latitude': {
                        'DataType': 'Number.float',
                        'StringValue': latitude
                    },
                    'longitude': {
                        'DataType': 'Number.float',
                        'StringValue': longitude
                    },
                    'heart_rate': {
                        'DataType': 'Number',
                        'StringValue': heart_rate
                    }
                }
            )
            # Print out the response
            print(response)


def read_message(message):
    testdata = StringIO(message)
    df = pd.read_csv(testdata, sep=",")

    # leggi le colonne acc
    column_acc = df.loc[df[' Sensor Type'] == 0]
    column_gir = df.loc[df[' Sensor Type'] == 1]

    column_acc_x = column_acc.iloc[:, 2].to_numpy()
    column_acc_y = column_acc.iloc[:, 3].to_numpy()
    column_acc_z = column_acc.iloc[:, 4].to_numpy()

    column_gir_x = column_gir.iloc[:, 2].to_numpy()
    column_gir_y = column_gir.iloc[:, 3].to_numpy()
    column_gir_z = column_gir.iloc[:, 4].to_numpy()

    return (column_acc_x, column_acc_y, column_acc_z,
            column_gir_x, column_gir_y, column_gir_z)


def remove_outlier_and_fix_missing(data, max_value, min_value):
    np.warnings.filterwarnings('ignore')
    data[data > max_value] = np.NaN
    data[data < min_value] = np.NaN

    # TODO: rimuovere NAN e sostituirli con media mobile
    # data = data.fillna(pd.rolling_mean(data, 6, min_periods=1))

    data = data[~np.isnan(data)]
    return data

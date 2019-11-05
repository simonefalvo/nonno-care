import boto3
import time
import random

PERIOD = 12  # Sample period
AVG_HRATE = 75
VAR_HRATE = 15


def main():
    sensor_id = 5
    register_user(sensor_id)
    counter = 0
    while True:
        counter += 1
        latitude = 41.858362
        longitude = 12.635893
        heart_rate = 112
        # add if random data send fall data
        fall = fall_data()
        send_message(sensor_id, latitude, longitude, heart_rate, fall)
        time.sleep(PERIOD)


def register_user(sensor_id):

    # Generate user data
    avg_hrate = int(random.gauss(AVG_HRATE, VAR_HRATE))
    var_hrate = VAR_HRATE
    safety_latitude = random.uniform(-90, 90)
    safety_longitude = random.uniform(-180, 180)
    # safety_radius = random.uniform(10, 15)

    # Store user data
    dynamodb = boto3.resource('dynamodb')
    dynamodb_client = boto3.client('dynamodb')
    print(dynamodb)
    table = dynamodb.Table('nonno-stack-UserDataTable-H33XU85CDKXD')
    #T0GLBM9HAHPQ virginia
    #VU3YVE27MISR  parigi
    print(table)

    response = dynamodb_client.describe_table(TableName='nonno-stack-UserDataTable-H33XU85CDKXD')

    print(response)

    response = table.put_item(
        Item={
            'sensor_id': str(sensor_id),
            'safety_latitude': str(safety_latitude),
            'safety_longitude': str(safety_longitude),
            'avg_hrate': str(avg_hrate),
            'var_hrate': str(var_hrate)
        }
    )
    print(response)


def fall_data():
    file_name = "UMAFall_Subject_01_ADL_Aplausing_1_2017-04-14_23-38-23.csv"
    #file_name = "UMAFall_Subject_04_Fall_lateralFall_3_2016-06-13_13-18-13.csv"
    with open(file_name) as f:
        s = f.read() + '\n'
    # print(s)
    return s


def send_message(sensor_id, latitude, longitude, heart_rate, fall):

    timestamp = time.time()

    # Create SQS client
    sqs = boto3.client('sqs')
    queue_url = "https://sqs.us-east-1.amazonaws.com/043090642581/nonno-stack-SQSQueue-1RUZP01BHLGVZ"

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageAttributes={
            'sensor_id': {
                'DataType': 'Number',
                'StringValue': str(sensor_id)
            },
            'timestamp': {
                'DataType': 'String',
                'StringValue': str(timestamp)
            },
            'latitude': {
                'DataType': 'Number.float',
                'StringValue': str(latitude)
            },
            'longitude': {
                'DataType': 'Number.float',
                'StringValue': str(longitude)
            },
            'heart_rate': {
                'DataType': 'Number',
                'StringValue': str(heart_rate)
            },
            'fall': {
                'DataType': 'String',
                'StringValue': fall
            }
        },
        MessageBody=(
            'test body'
        )
    )

    print(response['MessageId'])


def get_position(origin):
    return


def get_frequency(avg_hrate):
    return


if __name__ == '__main__':
    main()

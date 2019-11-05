import time
import boto3
import os


MAX_FREQ = 100


def handler(event, context):
    for record in event['Records']:
        print("test")
        payload = record["body"]
        attributes = record["messageAttributes"]
        print(str(payload))
        print(attributes)
        print(time.ctime(float(attributes["timestamp"]["stringValue"])))

        sensor_id = attributes["sensor_id"]["stringValue"]
        timestamp = attributes["timestamp"]["stringValue"]
        latitude = attributes["latitude"]["stringValue"]
        longitude = attributes["longitude"]["stringValue"]
        heart_rate = attributes["heart_rate"]["stringValue"]
        fall_data = attributes["fall"]["stringValue"]

        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table(os.environ['SENSOR_DATA_TABLE'])

        table.put_item(
            Item={
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'latitude': latitude,
                'longitude': longitude,
                'heart_rate': heart_rate,
                'fall': fall_data
            }
        )

        if len(fall_data) > 0:
            # Create an SNS client
            sns = boto3.client('sns')

            # Publish a simple message to the specified SNS topic
            response = sns.publish(
                TopicArn=os.environ['SNS_TOPIC_FALL_DETECTION'],
                Message='Fall Detection Data',
                MessageAttributes={
                    'fall_data': {
                        'DataType': 'String',
                        'StringValue': fall_data
                    },
                    'timestamp': {
                        'DataType': 'String',
                        'StringValue': timestamp
                    }
                }
            )

        if int(heart_rate) > MAX_FREQ:
            # Create an SNS client
            sns = boto3.client('sns')

            # Publish a simple message to the specified SNS topic
            response = sns.publish(
                TopicArn=os.environ['SNS_TOPIC_HEARTRATE'],
                Message='Hello World!',
                MessageAttributes={
                    'sensor_id': {
                        'DataType': 'Number',
                        'StringValue': sensor_id
                    },
                    'timestamp': {
                        'DataType': 'String',
                        'StringValue': timestamp
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

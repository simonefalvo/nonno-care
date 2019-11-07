import time
import boto3
import os


def handler(event, context):
    for record in event['Records']:
        attributes = record["Sns"]["MessageAttributes"]
        print(attributes)
        print(time.ctime(float(attributes["timestamp"]["Value"])))

        sensor_id = attributes["sensor_id"]["Value"]
        timestamp = attributes["timestamp"]["Value"]
        latitude = attributes["latitude"]["Value"]
        longitude = attributes["longitude"]["Value"]
        heart_rate = int(attributes["heart_rate"]["Value"])

        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['USER_DATA_TABLE'])

        response = table.get_item(
            Key={
                'sensor_id': sensor_id
            }
        )
        item = response['Item']
        print("Item:\n", item)

        avg_hrate = int(item['avg_hrate'])
        var_hrate = int(item['var_hrate'])

        if not avg_hrate - var_hrate <= heart_rate <= avg_hrate + var_hrate:
            print("WARNING: Abnormal Heartbeats")
            # Create an SNS client
            sns = boto3.client('sns')

            # Publish a simple message to the specified SNS topic
            response = sns.publish(
                TopicArn=os.environ['SNS_TOPIC_NOTIFY'],
                Message='Attenzione: anomalia cardiaca rilevata',
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
                        'StringValue': str(heart_rate)
                    }
                }
            )
            # Print out the response
            print(response)

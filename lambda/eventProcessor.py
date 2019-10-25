import time
import boto3


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

        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('nonno-stack-SensorDataTable-1HCL4T0PRUMEG')

        table.put_item(
            Item={
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'latitude': latitude,
                'longitude': longitude,
                'heart_rate': heart_rate
            }
        )

        if int(heart_rate) > MAX_FREQ:
            # Create an SNS client
            sns = boto3.client('sns')

            # Publish a simple message to the specified SNS topic
            response = sns.publish(
                TopicArn='arn:aws:sns:eu-west-3:043090642581:nonno-stack-SNSTopicHeartRate-19BJCJ8NNLJ1R',
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

import boto3
import os

ALPHA = 3/2


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    sns = None
    batch_size = len(event['Records'])
    for record in event['Records']:
        attributes = record["messageAttributes"]
        #print(attributes)
        sensor_id = attributes["sensor_id"]["stringValue"]
        timestamp = attributes["timestamp"]["stringValue"]
        latitude = attributes["latitude"]["stringValue"]
        longitude = attributes["longitude"]["stringValue"]
        heart_rate = int(attributes["heart_rate"]["stringValue"])

        table = dynamodb.Table(os.environ['USER_DATA_TABLE'])
        response = table.get_item(
            Key={
                'sensor_id': sensor_id
            }
        )
        item = response['Item']
        #print("Item:\n", item)

        avg_hrate = int(item['avg_hrate'])
        var_hrate = int(item['var_hrate'])

        if not avg_hrate - ALPHA * var_hrate <= heart_rate <= avg_hrate + ALPHA * var_hrate:
            if sns is None:
                # Create an SNS client
                sns = boto3.client('sns')
            # Publish a simple message to the specified SNS topic
            sns.publish(
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
                    'type': {
                        'DataType': 'String',
                        'StringValue': 'Anomalia cardiaca'
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
        else:
            print("JOB_ID {}, RequestId: {}, BatchSize: {}"
                  .format(sensor_id + timestamp.replace('.', '-'), context.aws_request_id, batch_size))

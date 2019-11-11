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

        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table(os.environ['SENSOR_DATA_TABLE'])
        item ={
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'latitude': latitude,
                'longitude': longitude,
                'heart_rate': heart_rate
            }

        if 'fall' in attributes:
            fall_data = attributes["fall"]["stringValue"]
            item['fall'] = fall_data

            message = "Possibile caduta"
            topic = os.environ['SNS_TOPIC_FALL_DETECTION']
            print(publish_topic(topic, message, sensor_id, timestamp, latitude, longitude, heart_rate, fall_data))

        if int(heart_rate) > MAX_FREQ:
            message = "Possibile anomalia cardiaca"
            topic = os.environ['SNS_TOPIC_HEARTRATE']
            print(publish_topic(topic, message, sensor_id, timestamp, latitude, longitude, heart_rate))

        table.put_item(Item=item)


# TODO: creare un layer
def publish_topic(topic, message, sensor_id, timestamp, latitude, longitude, heart_rate, fall_data=None):

    print("Topic dentro la funzione:", topic)
    # Create an SNS client
    sns = boto3.client('sns')

    attributes = {
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
    if fall_data is not None:
        attributes['fall'] = {
                'DataType': 'String',
                'StringValue': fall_data
            }

    # Publish a simple message to the specified SNS topic
    return sns.publish(
        TopicArn=topic,
        Message=message,
        MessageAttributes=attributes
    )

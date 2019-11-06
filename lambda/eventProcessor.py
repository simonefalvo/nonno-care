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
            message = "Possibile caduta"
            topic = os.environ['SNS_TOPIC_FALL_DETECTION']
            print(publish_topic(topic, message, sensor_id, timestamp, latitude, longitude, heart_rate, fall_data))

        if int(heart_rate) > MAX_FREQ:
            message = "Possibile anomalia cardiaca"
            topic = os.environ['SNS_TOPIC_HEARTRATE']
            print(publish_topic(topic, message, sensor_id, timestamp, latitude, longitude, heart_rate))


# TODO: creare un layer
def publish_topic(topic, message, sensor_id, timestamp, latitude, longitude, heart_rate, fall_data="ND"):
    print("Topic dentro la funzione:", topic)
    # Create an SNS client
    sns = boto3.client('sns')

    # Publish a simple message to the specified SNS topic
    return sns.publish(
        TopicArn=topic,
        Message=message,
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
            },
            'fall_data': {
                'DataType': 'String',
                'StringValue': fall_data
            }
        }
    )

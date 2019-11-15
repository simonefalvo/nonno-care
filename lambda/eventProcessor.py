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

        message = "Controllo posizione"
        topic = os.environ['SNS_TOPIC_POSITION']
        print(publish_topic(topic, "controllo posizione", message, sensor_id, timestamp,
                            latitude, longitude, heart_rate))

        if 'fall_data' in attributes:
            fall_data = attributes["fall_data"]["stringValue"]
            item['fall_data'] = fall_data

            message = "Possibile caduta"
            topic = os.environ['SNS_TOPIC_FALL_DETECTION']
            print(publish_topic(topic, "caduta", message, sensor_id, timestamp,
                                latitude, longitude, heart_rate, fall_data=fall_data))

        if int(heart_rate) > MAX_FREQ:
            message = "Possibile anomalia cardiaca"
            topic = os.environ['SNS_TOPIC_HEARTRATE']
            print(publish_topic(topic, "anomalia cardiaca", message, sensor_id, timestamp,
                                latitude, longitude, heart_rate))

        if 'sos' in attributes:
            item['sos'] = '1'
            message = "Richiesta di SOS "
            topic = os.environ['SNS_TOPIC_NOTIFY']
            print(publish_topic(topic, "richiesta SOS", message, sensor_id, timestamp,
                                latitude, longitude, heart_rate, sos=1))

        table.put_item(Item=item)


# TODO: creare un layer
def publish_topic(topic, notification_type, message, sensor_id, timestamp,
                  latitude, longitude, heart_rate, sos=None, fall_data=None):

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
        },
        'type': {
            'DataType': 'String',
            'StringValue': notification_type
        }
    }
    if fall_data is not None:
        attributes['fall_data'] = {
                'DataType': 'String',
                'StringValue': fall_data
            }
    if sos is not None:
        attributes['sos'] = {
                'DataType': 'String',
                'StringValue': '1'
            }

    print(attributes)
    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn=topic,
        Message=message,
        MessageAttributes=attributes
    )

    print("JOB_ID {}, RequestId: {}"
          .format(sensor_id + timestamp.replace('.', '-'), context.aws_request_id))

    return response

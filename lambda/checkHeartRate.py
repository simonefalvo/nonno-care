import time
import boto3


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
        table = dynamodb.Table('nonno-stack-UserDataTable-RMJMKMKYK11F')

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

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
        heart_rate = attributes["heart_rate"]["Value"]

        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('nonno-stack-UserDataTable-RMJMKMKYK11F')

        print("UserDataTable creation time:", table.creation_date_time)
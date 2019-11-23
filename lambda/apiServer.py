import boto3
import os
import json


def handler(event, context):
    """Provide an event that contains the following keys:
      - table: the name of the dynamodb table
      - operation: one of the operations in the operations dict below
      - payload: a parameter to pass to the operation being performed
    """

    # print("Received event: " + json.dumps(event, indent=2))

    event_body = json.loads(event['body'])
    print(event_body)
    table = event_body['table']
    operation = event_body['operation']

    tables = {
        'sensors': os.environ['SENSOR_DATA_TABLE'],
        'accidents': os.environ['ACCIDENT_DATA_TABLE']
    }

    dynamo = boto3.resource('dynamodb').Table(tables[table])

    operations = {
        'history': lambda x: dynamo.query(**x),
        'accidents': lambda x: dynamo.query(**x),
        'echo': lambda x: x,
        'ping': lambda x: 'pong'
    }

    if operation in operations:
        status_code = 200
        response_body = json.dumps({
                "message": operations[operation](event_body['payload'])
            })
        print(response_body)
    else:
        status_code = 400
        response_body = json.dumps({
                "message": "Unrecognized operation: {}".format(operation)
            })

    return {
        "statusCode": status_code,
        "body": response_body
    }

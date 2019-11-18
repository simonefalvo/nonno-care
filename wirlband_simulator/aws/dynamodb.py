import boto3


def put_item(table_name, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table.put_item(Item=item)

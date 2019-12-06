import os

import boto3
from botocore.exceptions import ClientError


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    ses = boto3.client('ses', region_name=os.environ['AWS_REGION'])
    batch_size = len(event['Records'])
    for record in event['Records']:
        message = record["body"]
        attributes = record["messageAttributes"]
        sensor_id = attributes["sensor_id"]["stringValue"]
        timestamp = attributes["timestamp"]["stringValue"]
        accident_type = attributes["type"]["stringValue"]
        latitude = attributes["latitude"]["stringValue"]
        longitude = attributes["longitude"]["stringValue"]
        heart_rate = int(attributes["heart_rate"]["stringValue"])

        # store accident data
        table = dynamodb.Table(os.environ['ACCIDENT_DATA_TABLE'])
        table.put_item(
            Item={
                'sensor_id': sensor_id,
                'typestamp': timestamp + '#' + accident_type,
                'latitude': latitude,
                'longitude': longitude,
                'heart_rate': heart_rate,
            }
        )

        # send email to subscribers
        email = get_subscribers(dynamodb, sensor_id)
        #print("Email: ", email)
        send_email(ses, email, message)

        print("JOB_ID {}, RequestId: {}, BatchSize: {}"
              .format(sensor_id + timestamp.replace('.', '-'), context.aws_request_id, batch_size))


def get_subscribers(dynamodb, sensor_id):
    table = dynamodb.Table(os.environ['USER_DATA_TABLE'])

    response = table.get_item(
        Key={
            'sensor_id': sensor_id
        }
    )
    return response['Item']['email']


def send_email(ses_client, recipient, message):
    sender = "Nonno Care <nonnocare.notify@gmail.com>"
    subject = "nonno ALERT"

    # The email body for recipients with non-HTML email clients.
    body_text = message

    # The HTML body of the email.
    body_html = """<html>
    <head></head>
    <body>
      <h1>{}</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """.format(message)

    # The character encoding for the email.
    charset = "UTF-8"

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:".format(response['MessageId']))

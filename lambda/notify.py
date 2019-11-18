import os
import smtplib
import ssl
import logging

import boto3
from botocore.exceptions import ClientError


def handler(event, context):
    for record in event['Records']:
        message = record["Sns"]["Message"]
        attributes = record["Sns"]["MessageAttributes"]
        sensor_id = attributes["sensor_id"]["Value"]
        timestamp = attributes["timestamp"]["Value"]
        accident_type = attributes["type"]["Value"]
        latitude = attributes["latitude"]["Value"]
        longitude = attributes["longitude"]["Value"]
        heart_rate = int(attributes["heart_rate"]["Value"])

        print(message)

        # store accident data
        table = boto3.resource('dynamodb').Table(os.environ['ACCIDENT_DATA_TABLE'])
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
        email = get_subscribers(sensor_id)
        print("Email: ", email)
        send_smtp(email, message)
        #send_email(email, message)

        print("JOB_ID {}, RequestId: {}"
              .format(sensor_id + timestamp.replace('.', '-'), context.aws_request_id))


def get_subscribers(sensor_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['USER_DATA_TABLE'])

    response = table.get_item(
        Key={
            'sensor_id': sensor_id
        }
    )
    return response['Item']['email']


def send_email(recipient, message):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    sender = "Nonno Care <nonnocare.notify@gmail.com>"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    aws_region = "eu-west-3"

    # The subject line for the email.
    subject = "nonno ALERT"

    # The email body for recipients with non-HTML email clients.
    body_text = message

    # The HTML body of the email.
    body_html = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """

    # The character encoding for the email.
    charset = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=aws_region)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
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
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def send_smtp(to_address, message):
    from_address = "nonnocare.notify@gmail.com"
    password = "NonCar99"
    email = """Subject: NONNO ALERT 

    {}"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_address, password)
        server.sendmail(from_address, to_address, email.format(message))

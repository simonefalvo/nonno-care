import boto3


def verify_email(address):
    # Create SES client
    ses = boto3.client('ses')

    response = ses.verify_email_identity(
      EmailAddress=address
    )

    print(response)


if __name__ == '__main__':
    verify_email("nonnocare.notify@gmail.com")

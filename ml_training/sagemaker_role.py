import boto3
import json


def create_role_sagemaker():

    # Create IAM client
    iam = boto3.client('iam')

    path = '/'
    role_name = 'AmazonSageMaker-ExecutionRole-20191202T162997'
    arn_sagemaker_full_access = 'arn:aws:iam::aws:policy/AmazonSageMakerFullAccess'
    policy_execution = 'AmazonSageMaker-ExecutionPolicy'
    policy_s3 = 'S3-Sagemaker'
    description = 'A test Role'

    try:

        my_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                  "Sid": "",
                  "Effect": "Allow",
                  "Principal": {
                    "Service": "sagemaker.amazonaws.com"
                  },
                  "Action": "sts:AssumeRole"
                }
            ]
        }

        tags = [
            {
                'Key': 'Environment',
                'Value': 'Production'
            }
        ]

        response = iam.create_role(
            Path=path,
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(my_policy),
            Description=description,
            MaxSessionDuration=3600,
            Tags=tags
        )

        arn = response['Role']['Arn']
        print("ARN: ", arn)

        response = iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=arn_sagemaker_full_access
        )

        policy_execution_role = \
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "s3:GetObject",
                            "s3:PutObject",
                            "s3:DeleteObject",
                            "s3:ListBucket"
                        ],
                        "Resource": [
                            "arn:aws:s3:::*"
                        ]
                    }
                ]
            }

        response_execution_policy = iam.create_policy(
            PolicyName=policy_execution,
            Path=path,
            PolicyDocument=json.dumps(policy_execution_role)
        )

        response = iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=response_execution_policy['Policy']['Arn']
        )

        policy_s3_sagemaker =\
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "VisualEditor0",
                        "Effect": "Allow",
                        "Action": [
                            "s3:PutAccountPublicAccessBlock",
                            "s3:GetAccountPublicAccessBlock",
                            "s3:ListAllMyBuckets",
                            "s3:ListJobs",
                            "s3:CreateJob",
                            "s3:HeadBucket"
                        ],
                        "Resource": "*"
                    },
                    {
                        "Sid": "VisualEditor1",
                        "Effect": "Allow",
                        "Action": "s3:*",
                        "Resource": [
                            "arn:aws:s3:::*",
                            "arn:aws:s3:::*/*",
                            "arn:aws:s3:*:*:job/*"
                        ]
                    }
                ]
            }

        response_execution_policy_s3 = iam.create_policy(
            PolicyName=policy_s3,
            Path=path,
            PolicyDocument=json.dumps(policy_s3_sagemaker)
        )

        response = iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=response_execution_policy_s3['Policy']['Arn']
        )

        return arn

    except Exception as e:
        print(e)


if __name__ == '__main__':
    arn = create_role_sagemaker()
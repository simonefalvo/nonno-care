import boto3

role_name = 'AmazonSageMaker-ExecutionRole-20191202T162997'
policy_execution = 'AmazonSageMaker-ExecutionPolicy'
policy_s3 = 'S3-Sagemaker'

iam = boto3.client('iam')

try:
    list_policies = iam.list_attached_role_policies(
        RoleName=role_name,
        MaxItems=4
    )
    for policy in list_policies['AttachedPolicies']:
        # sgancio le policy dal ruolo per poi poterle rimuovere
        iam.detach_role_policy(
            RoleName=role_name,
            PolicyArn=policy['PolicyArn']
        )
        # rimuovo le policy da me create
        if policy['PolicyName'] == policy_execution or policy['PolicyName'] == policy_s3:

            response = iam.delete_policy(
                PolicyArn=policy['PolicyArn']
            )
            print("Deleted policy {}".format(policy['PolicyName']))

    response = iam.delete_role(
        RoleName=role_name
    )

except iam.exceptions.NoSuchEntityException:
    pass
except:
    print("An error occurred while trying to remove the role {}".format(role_name))
else:
    print("Deleted role {}".format(role_name))

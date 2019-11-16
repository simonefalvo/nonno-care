import boto3


def stack_output(stack_name, output_key):
    cf = boto3.client('cloudformation')
    description = cf.describe_stacks(StackName=stack_name)
    stack = description['Stacks'][0]
    outputs = stack['Outputs']
    for output in outputs:
        if output['OutputKey'] == output_key:
            return output['OutputValue']
    raise NameError(output_key)

# nonno-care

description

## Getting Started

### Prerequisites
* [AWS Command Line Interface](https://aws.amazon.com/cli/)
* [Python3.6](https://www.python.org/)

## Deployment
Package the local artifacts (local paths) that the AWS CloudFormation template references
```
$ aws cloudformation package --template-file template.yaml --output-template packaged.yaml --s3-bucket nonno-care
```

Deploy the specified AWS CloudFormation template
```
$ aws cloudformation deploy --template-file packaged.yaml --region eu-west-3 --capabilities CAPABILITY_IAM --stack-name nonno-stack
```

## Running

### Running Example


## Authors

* **Falvo Simone**
* **Pietrangeli Aldo**

## License


## Acknowledgments

# AWS G4 Gaming Box

This project will deploy G4 EC2 windows instance. The instance is running [NICEDCV server](https://docs.aws.amazon.com/dcv/latest/userguide/getting-started.html) and is bootstrapped with following applications and drivers:
* NVIDIA gaming drivers for G4 instances
* Steam app
* Parsec app
* Google Chrome
* 7Zip
* AWSCLI

## Pre-Requisites

The following dependencies must be installed:
- awscli
- Python >=3.8 and pip ([Local Development only](#local-development))
- virtualenv ([Local Development only](#local-development))

## Deploy the CloudFormation Stack
As the solution is using `Lambda` function, the code needs to be zipped and uploaded to S3 bucket. The `Makefile` will install lambda libraries, package the template to S3 bucket and finally deploy the CloudFormation stack.

1. Set the env variables
    ```shell script
    BUCKET_NAME=""
    AWS_REGION=""
    KEY_PAIR_NAME=""
    ```
1. Create S3 bucket
    ```shell script
    aws s3 mb s3://${BUCKET_NAME} --region ${AWS_REGION}
    ```
1. Create Amazon EC2 key pair
    Specify the location where to store pem file after `>`
    ```shell script
    aws ec2 create-key-pair --key-name ${KEY_PAIR_NAME} --query 'KeyMaterial' --output text > ~/Downloads/${KEY_PAIR_NAME}.pem --region ${AWS_REGION}
    ```
1. Set the permission of the `.pem` file to read only
    ```shell script
    chmod 400 ~/Downloads/${KEY_PAIR_NAME}.pem
    ```
1. Create a `.custom.mk` file and populate it with your own values
   ```shell script
   cp .custom.mk.example .custom.mk
   ```

   |Variable Label|Example|Description|
   |--------------|-------|-----------|
   |AWS_REGION |eu-west-2|The AWS region to deploy the solution to|
   |BUCKET_NAME|my-unique-bucket-name|Use the same value from step above|
   |STACK_NAME |GamingBox|The name of the stack|
   |GAMING_BOX_INSTANCE_TYPE |g4dn.xlarge|The type of the instance from a G4 family|
   |KEY_PAIR   |MyKeyPair|The name of the KeyPair created above|
   |ON_PREM_IP |0.0.0.0/0|CIDR annotation of your home IPv4 address|

1. Deploy the stack
    ```shell script
    make deploy
    ```
1. Go to AWS console and wait for the stack to complete
1. Navigate to the EC2 console, select the Gaming instance and click on **Connect**
1. Note down the **Public DNS**, **User name** and **Password** (you may have to wait a few minutes for the password to become available)

## Connect to the Gaming Server
1. Get NICE DCV Client from [https://docs.aws.amazon.com/dcv/latest/userguide/client.html](https://docs.aws.amazon.com/dcv/latest/userguide/client.html)
1. Connect via DCV client, providing login details noted above

## What will happen when you are done gaming?
[TODO]
- Architecture diagram
- Description how lambda will create snapshot and AMI

## Gaming box start up script
[TODO]
- start the game box using Launch Configuration and AMI created by lambda function
    ```shell script
    start-gaming-box -r eu-west-2 -l lt-0xxxxxxx -v 1 -i g4dn.xlarge
    ```
- parameters
    ```shell script
    start_server.sh [OPTION]
    -r; AWS Region (default: eu-west-1)
    -l; Set Launch Template ID (required)
    -v; Launch template version (default: 1)
    -i; Instance Type (default: gdn.4xlarge)
    -h; Help
    ```

## Local Development
This section details how to run the solution locally and deploy your code changes from the command line.

### Initialize env
1. Install the extra prerequisites for development.
1. Follow the steps 1. to 5. from [Deploy the CloudFormation Stack](#Deploy-the-CloudFormation-Stack)
1. Initialize the local environment
    ```shell script
    make init
    ```
1. Activate `virtualenv` environment.
    ```shell script
    source venv/bin/activate
    ```

### Test changes
The following command will run `pre-commit` tests. This should be run before every new commit.
```shell script
make test
```

### Clean the virtual environment
This command will delete the virtual environment and all installed packages install via `make init`
```shell script
make clean
```

### Delete the resources created via CloudFormation
Below command will delete deployed stack
```shell script
make delete
```

# AWS G4 Gaming Box

> Under development, install at your own risk!

## Pre-req
1. Install `AWS CLI`
1. Install `pip`

## Deploy the CloudFormation Stack
As the solution is using `Lambda` function, the code needs to be zipped and uploaded to S3 bucket. The `deploy.sh` script will install lambda libraries, will package the template to S3 bucket and finaly will deploy the CloudFormation stack.

1. Create Amazon S3 bucket
   ```
   $ BUCKET_NAME=""
   $ AWS_REGION=""
   $ aws s3 mb s3://${BUCKET_NAME} --region $AWS_REGION
   ```
1. Create Amazon EC2 key pair
   Replace the `--key-name` with your own key name and specify the location after `>`
   ```
   aws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > ~/Downloads/MyKeyPair.pem --region $AWS_REGION
   ```
1. Set the permission of the `.pem` file to read only
   ```
   chmod 400 ~/Downloads/MyKeyPair.pem
   ```
1. Create an `.env` file and populate it with your own values

   ```
   $ cp .env.example .env
   ```

   |Variable Label|Example|Description|
   |--------------|-------|-----------|
   |BUCKET_NAME|my-unique-bucket-name|Use the same value from step above|
   |PREFIX_NAME|gaming-box-infra|This will put all the code in a bucket folder|
   |STACK_NAME |GamingBox|The name of the stack|
   |AWS_REGION |eu-west-2|The AWS region to deploy the solution to|
   |KEY_PAIR   |MyKeyPair|The name of the KeyPair created above|
   |ON_PREM_IP |0.0.0.0/0|CIDR annotation of your home IP, to increase the security|

1. Double check that `deploy.sh` is executable, if not run:
   ```
   $ chmod +x deploy.sh
   ```
1. Run the deployment script
   ```
   $ ./deploy.sh
   ```
1. Go to AWS console and wait for the stack to complete
1. Navigate to the EC2 console, select the Gaming instance and click on **Connect**
1. Note down the **Public DNS**, **User name** and **Password** (you may have to wait a few minutes for the password to become available)

## Connect to the Gaming Server
1. Get NICE DCV Client from [https://docs.aws.amazon.com/dcv/latest/userguide/client.html](https://docs.aws.amazon.com/dcv/latest/userguide/client.html)
1. Connect via DCV client, providing login details noted above

## Install Parsec
1. Open PowerShell and paste command bellow:
```powershell
[Net.ServicePointManager]::SecurityProtocol = "tls12, tls11, tls"
(New-Object System.Net.WebClient).DownloadFile("https://github.com/jamesstringerparsec/Parsec-Cloud-Preparation-Tool/archive/master.zip","$ENV:UserProfile\Downloads\Parsec-Cloud-Preparation-Tool.zip")
New-Item -Path $ENV:UserProfile\Downloads\Parsec-Cloud-Preparation-Tool -ItemType Directory
Expand-Archive $ENV:UserProfile\Downloads\Parsec-Cloud-Preparation-Tool.Zip -DestinationPath $ENV:UserProfile\Downloads\Parsec-Cloud-Preparation-Tool
CD $ENV:UserProfile\Downloads\Parsec-Cloud-Preparation-Tool\Parsec-Cloud-Preparation-Tool-master\
Powershell.exe -File $ENV:UserProfile\Downloads\Parsec-Cloud-Preparation-Tool\Parsec-Cloud-Preparation-Tool-master\Loader.ps1

```
1. Follow installation instructions from Parsec Team blog post [RTX Cloud Gaming With The New AWS G4 Instances](https://blog.parsecgaming.com/rtx-cloud-gaming-with-the-new-aws-g4-instances-11d1c60c2d09)

## What will happen when you are done gaming?
[TODO]
- Architecture diagram
- Description how lambda will create snapshot and AMI

## Gaming box start up script

    $ start-gaming-box -r eu-west-2 -l lt-0xxxxxxx -v 1 -i g4dn.4xlarge

    start_server.sh [OPTION]
    -r; AWS Region (default: eu-west-1)
    -l; Set Launch Template ID (required)
    -v; Launch template version (default: 1)
    -i; Instance Type (default: gdn.4xlarge)
    -h; Help

#!/usr/bin/env bash

# Import configuration
. .env

# Install Lambda dependencies
pip install -r snapshotter/requirements.txt --target snapshotter -U

printf "\n--> Packaging and uploading templates to the %s S3 bucket ...\n" $BUCKET_NAME

aws cloudformation package \
  --template-file ./gaming-box.template \
  --s3-bucket $BUCKET_NAME \
  --s3-prefix $PREFIX_NAME \
  --region $AWS_REGION \
  --output-template-file ./gaming-box-packaged.template

printf "\n--> Deploying %s template...\n" $STACK_NAME

aws cloudformation deploy \
  --template-file gaming-box-packaged.template \
  --stack-name $STACK_NAME \
  --region $AWS_REGION \
  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
  --parameter-overrides \
    KeyPair=${KEY_PAIR} \
    OnPremIp=${ON_PREM_IP}

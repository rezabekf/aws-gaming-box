#!/usr/bin/env bash

# Initialize variables in case flag is not provided
GAMING_INSTANCE_NAME="GamingBox"
LAUNCH_TEMPLATE=""
VERSION="1"
AWS_REGION="eu-west-1"
INSTANCE_TYPE="g4dn.4xlarge"

# Get the command base name
cmd() {
  echo "$(basename $0)"
}

# Usage
usage() {
  echo "\
    $(cmd) [OPTION]
     -r; AWS Region (default: eu-west-1)
     -l; Set Launch Template ID (required)
     -v; Launch template version (default: 1)
     -i; Instance Type (default: gdn.4xlarge)
     -h; Help
  " | column -t -s ";"
}

# Set the getopts flags
while getopts "r:l:v:i:h" opt; do
  case "$opt" in
  r)
    AWS_REGION=${OPTARG}
    ;;
  l)
    LAUNCH_TEMPLATE=${OPTARG}
    ;;
  v)
    VERSION=${OPTARG}
    ;;
  i)
    INSTANCE_TYPE=${OPTARG}
    ;;
  h)
    usage
    exit 2
    ;;
  esac
done

# Get the AMI ID based on the tag value
echo "Getting latest AMI ID in ${AWS_REGION}"
AMI=$(aws ec2 describe-images \
  --filters Name=name,Values="${GAMING_INSTANCE_NAME}" \
  --output text \
  --query 'Images[*].{ID:ImageId}' \
  --region ${AWS_REGION})

# Launch the EC2 instance from the launch template
echo "Launching new instance with AMI id: $AMI"
INSTANCE_ID=$(aws ec2 run-instances \
  --launch-template LaunchTemplateId=${LAUNCH_TEMPLATE},Version=${VERSION} \
  --image-id ${AMI} \
  --instance-type ${INSTANCE_TYPE} \
  --query 'Instances[].[InstanceId]' \
  --output text \
  --region ${AWS_REGION})

echo "Instance ID: $INSTANCE_ID has been launched!"

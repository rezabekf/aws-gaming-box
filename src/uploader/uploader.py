from __future__ import print_function

import logging
import os

import boto3
from botocore.exceptions import ClientError
from crhelper import CfnResource

logger = logging.getLogger(__name__)
helper = CfnResource(
    json_logging=False, log_level="DEBUG", boto_level="CRITICAL", sleep_on_delete=120
)
s3 = boto3.client("s3")
script_folder = "./scripts/"


@helper.create
def create(event, context):
    logger.info("Got Create")
    properties = event.get("ResourceProperties", {})
    bucket_name = properties.get("AssetsS3Bucket")

    for file in _get_scripts(script_folder):
        _upload_file(script_folder + file, bucket_name, file)

    return helper.PhysicalResourceId


@helper.update
def update(event, context):
    logger.info("Got Update")


@helper.delete
def delete(event, context):
    logger.info("Got Delete")
    properties = event.get("ResourceProperties", {})
    bucket_name = properties.get("AssetsS3Bucket")

    for file in _get_scripts(script_folder):
        _delete_file(bucket_name, file)


def handler(event, context):
    helper(event, context)


def _get_scripts(folder):
    scripts = []
    for path, directories, files in os.walk(folder):
        for filename in files:
            scripts.append(filename)
    return scripts


def _upload_file(file_name, bucket, object_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def _delete_file(bucket_name, file_name):
    s3.delete_object(
        Bucket=bucket_name,
        Key=file_name,
    )

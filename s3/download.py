import os
import boto3
import botocore
import logging


def download_receipt(file_name, bucket, local_file):

    s3 = boto3.resource('s3', aws_access_key_id=os.environ['ACCESS_KEY'],
                      aws_secret_access_key=os.environ['SECRET_KEY'])

    try:
        s3.Bucket(bucket).download_file(file_name, local_file)
    except botocore.ClientError as e:
        if e.response['Error']['Code'] == "404":
            logging.log(logging.INFO, "The object does not exist.")
        else:
            raise
import boto3,botocore
from boto3.session import Session
session = Session()
s3 = session.resource('s3')
s3_client = session.client('s3')
BUCKET_NAME = "aub3data"
BUCKET = s3.Bucket(BUCKET_NAME)
AMI = ''
USER = "ubuntu"
HOST = "52.91.48.37"
private_key = "~/.ssh/cs5356"
S3BUCKET = ""
CONFIG_PATH = __file__.split('settings.py')[0]


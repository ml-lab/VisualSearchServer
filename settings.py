import boto3,botocore
from boto3.session import Session
import sys
session = Session()
s3 = session.resource('s3')
s3_client = session.client('s3')
BUCKET_NAME = "aub3data"
BUCKET = s3.Bucket(BUCKET_NAME)
AMI = ''
USER = "ubuntu"
HOST = "52.91.54.53"
private_key =  "~/.ssh/cs5356" # "~/.ssh/cornellaub3nca.pem" #
S3BUCKET = ""
CONFIG_PATH = __file__.split('settings.py')[0]
AWS = sys.platform != 'darwin'
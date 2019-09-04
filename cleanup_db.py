from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import pandas as pd
import datetime


client = boto3.client(
    'dynamodb',
    aws_access_key_id='AKIAJYE675YLK6PXNULA',
    aws_secret_access_key='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'
)

response = client.scan(TableName = 'MichiganPlusOne')

print(pd.DataFrame(response['Items']))

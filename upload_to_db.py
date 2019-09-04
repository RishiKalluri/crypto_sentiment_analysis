from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import pandas as pd

def upload_to_dynamo(new_data):
    client = boto3.client(
        'dynamodb',
        aws_access_key_id='AKIAJYE675YLK6PXNULA',
        aws_secret_access_key='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'
    )
    print("Beginning Upload")

    for i, x in new_data.iterrows():
        client.put_item(
           Item={
                'sentiment': {
                    'N': str(x['sentiment'])
                },
                'url': {
                    'S': x['url']
                },
                'article_date': {
                    'S': x['date']
                }
            },
            ReturnConsumedCapacity = 'TOTAL',
            TableName = 'MichiganPlusOne'
        )

    print("Upload Complete")

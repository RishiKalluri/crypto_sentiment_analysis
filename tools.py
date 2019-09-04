import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions

def iam_watson_key():
    with open('apiKey.json') as data_file:
        iam_info = json.load(data_file)
    print(iam_info["apiKey"])
    return iam_info["apiKey"]

def init_watson():
    return NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey=iam_watson_key(),
        url='https://gateway.watsonplatform.net/natural-language-understanding/api'
    )

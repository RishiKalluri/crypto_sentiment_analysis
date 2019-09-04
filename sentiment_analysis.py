import json

import pandas as pd
from tools import init_watson
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions
from statistics import mean

key_target_idx = {'ethereum' : 0, 'ETH': 1, 'buy': 2, 'sell': 3}

def parse_sentiment(response, return_list):
    for res in response["sentiment"]["targets"]:
        return_list[res["text"]] = res["score"]


def get_analysis(targets, url, watson_nlp): #single url, list of target keys, should return dict/list of corresponding sentiment values for each url
    try:
        return_list = {'ethereum': 0, 'ETH':0, 'buy': 0, 'sell': 0}
        response = watson_nlp.analyze(
            url=url,
            features=Features(sentiment=SentimentOptions(targets = targets))).get_result()
        parse_sentiment(response, return_list)

        return return_list
    except:
        return {'ethereum': 0, 'ETH':0, 'buy': 0, 'sell': 0}

def run_analysis(targets, urls, watson_nlp):
    all_sents = []
    for url in urls:
        sent_list = get_analysis(targets, url, watson_nlp)
        all_sents.append(sent_list)

    sent_data = pd.DataFrame(all_sents)

    return {"mean_bitcoin": mean(sent_data['ethereum']), "mean_btc": mean(sent_data['ETH']), "mean_buy": mean(sent_data['buy']), "mean_sell": mean(sent_data['sell'])}
    #loop through sent values in db

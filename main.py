from flask import Flask, jsonify
from tools import init_watson
import pandas as pd
import json
import datetime
import requests

from article_scraper import get_articles

# from webscraper import scrape_web
from sentiment_analysis import run_analysis
# from alexa_tooling import deliver_result
# from tools import cleanup_data
# import resource

from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

# app = Flask(__name__)
#
#
# @app.route("/", methods = ['GET'])
def parse_date(date):
  d = date.split('/')
  d.insert(0, d.pop())
  return '-'.join(d)

def convert_date(date_in):
    date_in = str(date_in).split(' ')[0]
    date_in = date_in.split('-')
    date_in.append(date_in.pop(0))
    return '/'.join(date_in)

def get_btc(start_date):
  parsed_start = parse_date(start_date)

  payload = {"start": parsed_start, "end": parsed_start}

  response = requests.get(" https://api.coindesk.com/v1/bpi/historical/close.json", params=payload)
  r = json.loads(response.text)
  return r["bpi"][parsed_start]


def evaluate():
    watson_nlp = init_watson()
    X_train = []
    y_train = []
    base = datetime.datetime.today() - datetime.timedelta(days=1)
    dates = [base - datetime.timedelta(days=x) for x in range(0, 20)]

    new_dates = []

    for date in dates:
        new_dates.append(convert_date(date))

    for date in new_dates:
        urls = get_articles("ethereum", date, date)
        mean_for_date = run_analysis(['ethereum', 'ETH', 'buy', 'sell'], urls, watson_nlp)
        btc_price = get_btc(date)
        X_train.append(mean_for_date)
        y_train.append(btc_price)
    X_train = pd.DataFrame(X_train)
    y_train = pd.DataFrame(y_train)

    print(X_train)

    model = KNeighborsRegressor()

    X_tr, X_te, y_tr, y_te = train_test_split(X_train, y_train, test_size = 0.2, random_state = 42)

    model.fit(X_tr, y_tr)
    accuracy = model.score(X_te, y_te)

    current_day = datetime.datetime.today()
    current_day = convert_date(current_day)
    current_urls = get_articles("ethereum", current_day, current_day)
    curr_mean_for_date = run_analysis(['ethereum', 'ETH', 'buy', 'sell'], current_urls, watson_nlp)

    X_predict = pd.DataFrame([curr_mean_for_date])

    regress_predict = model.predict(X_predict)

    print("Expected price of bitcoin will be roughly: " + str(regress_predict))
    curr_btc = json.loads(requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").text)["bpi"]["USD"]["rate_float"]
    if(regress_predict > curr_btc):
        print("BTC price expected to increase")
    else:
        print("BTC price expected to decrease")


    #scrape_web()
    #deliver_result()
    #cleanup_data()

evaluate()

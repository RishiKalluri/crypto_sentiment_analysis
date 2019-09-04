import re
import requests
import urllib3
from bs4 import BeautifulSoup

def get_articles(coin, start_date, end_date):

    # Ignores the following error:
    # urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='www.google.dz', port=443): Max retries exceeded with url
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Recieves query and performs Google Search for N amount of articles pertaining to the query
    phrase = "https://www.google.com/search?q=" + coin
    news_option = "&tbm=nws"
    results = "&num=100"
    date_range= "&tbs=cdr:1,cd_min:" + start_date + ",cd_max:" + end_date
    tbs_arg = 'cdr:1,cd_min:' + start_date + ',cd_max:' + end_date


    base_url = 'https://www.google.com/search'

    payload = {'q': coin, 'tbm': 'nws', 'num': 10, 'tbs': tbs_arg, 'as_epq': 'bitcoin'}

    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36" }

    google_url =  phrase + news_option + results + date_range
    page = requests.get(base_url, params=payload, headers=headers, verify=False)
    html_content = BeautifulSoup(page.content, features="html.parser")
    #print(google_url)
    #print(html_content)

    ret_links = []
    all_links = html_content.find_all('a', class_="lLrAF")
    for link in all_links:
        str_link = str(link)
        start = str_link.find("href")
        end = str_link.find("ping")
        ret_links.append(str_link[start+6:end-2])


    return ret_links

get_articles("bitcoin", "04/25/2019", "04/25/2019")

# -- coding: utf-8 --
from flask import Flask, request
from faker import Factory
import requests

app = Flask(__name__)


@app.route('/getCoInfo')
def search():
    ua = Factory.create().user_agent()
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json',
        'User-Agent': ua,
        'Host': 'app.gsxt.gov.cn'
    }
    url = 'http://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page=1'
    payload = {"searchword": "915000007935261598",
               "conditions": '{"excep_tab": "0", "ill_tab": "0", "area": "0", "cStatus": "0", "xzxk": "0", "xzcf": "0","dydj": "0"}',
               "sourceType": "A"
               }

    response = requests.request("POST", url, headers=headers, data=payload)

    # url = "http://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page=1"
    # payload = {'searchword': '915000007935261598',
    #            'conditions': '{"excep_tab": "0","ill_tab": "0","area": "0","cStatus": "0","xzxk": "0","xzcf": "0","dydj": "0"}',
    #            'sourceType': 'A'}
    # headers = {
    #     'X-Requested-With': 'XMLHttpRequest',
    #     'Accept': 'application/json',
    #     'User-Agent': ua,
    #     'Host': 'app.gsxt.gov.cn'
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()

def detail(ppid):
    pass

if __name__ == '__main__':
    app.debug = True
    app.run()

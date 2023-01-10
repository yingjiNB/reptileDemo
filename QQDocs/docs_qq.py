import requests
from faker import Factory
from typing import Dict

if __name__ == '__main__':
    url = 'https://docs.qq.com/dop-api/get/sheet?u=99e02012d6ee4e4183de717d9c2bb5c4&padId=300000000%24JOqyzUHrbprr&subId=BB08J2&startrow=61&endrow=803&xsrf=f0cbce179a67d8a5&_r=0.07240903694478318&outformat=1&normal=1&preview_token=&nowb=1&enableSmartsheetSplit=1&rev=461'
    ua = Factory.create().user_agent()
    headers = {
        'user-agent': ua,
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
        "cookie": "fingerprint=e6a7e53ad7734ed5a461a1e175c0bbd280; pgv_info=ssid=s3883427787; pgv_pvid=7833363163; pac_uid=0_cfa801330bef9; traceid=f0cbce179a; TOK=f0cbce179a67d8a5; hashkey=f0cbce17; ES2=39f728989fe92dc0; backup_cdn_domain=docs.gtimg.com; low_login_enable=1; optimal_cdn_domain=docs2.gtimg.com; DOC_SID=6f6c9388bd38413d8f159ff4b0597049d40066014a814490b8f26e5ef70a49ab; SID=6f6c9388bd38413d8f159ff4b0597049d40066014a814490b8f26e5ef70a49ab; loginTime=1672904911928",
        "referer": "https://docs.qq.com/sheet/DSk9xeXpVSHJicHJy?tab=BB08J2",
        "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-30fd8b33ccc856e33e361080c31bf8ad-19fc4415c0b2a8c3-01",
        "user-agent": ua
    }
    response = requests.get(url=url, headers=headers).json()
    data_dic: Dict[str, str] = response['data']['initialAttributedText']['text'][0][0][0]['c'][1]
    data_list = []
    count = 0
    last_key = 0

    for k, v in data_dic.items():
        new_data = {}

        last_key = k

        #
        # if int(k) - int(last_key) == 8:
        #     print(k)

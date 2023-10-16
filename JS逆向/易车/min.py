# -- coding: utf-8 --
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")

import execjs
import requests
import json

f = open('易车.js', 'r', encoding="utf-8")
js_code = f.read()
f.close()

js = execjs.compile(js_code)

dic = {'cityId': '2401', 'serialId': '7219'}
headers = js.call("get_headers", dic)

print(headers)

headers[
    'user-agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
headers['referer'] = "https://car.yiche.com/dibadaiyage/peizhi/"
headers[
    'Cookie'] = "isWebP=true; locatecity=310100; bitauto_ipregion=101.87.131.240%3A%E4%B8%8A%E6%B5%B7%E5%B8%82%3B2401%2C%E4%B8%8A%E6%B5%B7%2Cshanghai; CIGUID=e79cb639-097c-41fc-b867-1e0d788b0c78; CIGDCID=NWef5P5dmr4jdBaM7H2fwjN3ZKjjb6Mn; auto_id=ea198fff8d3e321786856c4a0402cd44; UserGuid=e79cb639-097c-41fc-b867-1e0d788b0c78; Hm_lvt_610fee5a506c80c9e1a46aa9a2de2e44=1697467507; selectcity=310100; selectcityid=2401; selectcityName=%E4%B8%8A%E6%B5%B7; exdltracker_url_index=17_28_1_4877_3_2; dltracker_url_index=; exdltracker_url_sIndex=17_28_1_4877_3_2; dltracker_url_sIndex=; externalrfpa_tracker=17_28_1_4877_3; externalrfpa_tracker_Record=17_28_1_4877_3; exdltracker_Record=17_28_1_4877_3_2; csids=7219;"

url = "https://mapi.yiche.com/web_api/car_model_api/api/v1/car/config_new_param"
params = {
    "cid": "508",
    "param": json.dumps(dic, separators=(',', ':'))
}
resp = requests.get(url, params=params, headers=headers)
print(resp.text)
with open("che.json", mode="w", encoding="utf-8") as f:
    f.write(resp.text)
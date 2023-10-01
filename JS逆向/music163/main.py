# -- coding: utf-8 --
import subprocess  # 执行命令行的
from functools import partial  # 固定某个参数的

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

import requests
import execjs

params = {
    "csrf_token": "",
    "encodeType": "aac",
    "ids": "[2076511018]",
    "level": "standard",
}
f = open('使用第三方库扣取.js', mode="r", encoding="utf-8")
js_code = f.read()
f.close()

js = execjs.compile(js_code)
ret = js.call('fn',params)

data = {
    "params": ret['encText'],
    "encSecKey": ret['encSecKey']
}

url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

session = requests.session()
session.headers = headers

resp = session.post(url, data=data, verify=False)

dic = resp.json()
print(dic)
for item in dic['data']:
    song_url = item['url']
    song_id = item['id']
    song_resp = session.get(song_url)
    with open(f"{song_id}.m4a", mode="wb") as f:
        f.write(song_resp.content)

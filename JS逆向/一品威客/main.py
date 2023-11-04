# -- coding: utf-8 --
import subprocess  # 执行命令行的
from functools import partial  # 固定某个参数的

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

import requests
import execjs

f = open('一品威客.js', mode="r", encoding="utf-8")
js_code = f.read()
f.close()
js = execjs.compile(js_code)

data = {
    "username": '11111111111',
    "password": 'qweasd',
    "code": 'qy4m',
    "hdn_refer": 'https://www.epwk.com/'
}

session = requests.session()
session.headers = js.call('fn', data)
session.headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
session.headers[
    'Cookie'] = "Hm_lvt_387b8f4fdb89d4ea233922bdc6466394=1699021134; PHPSESSID=378348132f8a1484ffa91552d243c96e5d00fedb; time_diff=-1; XDEBUG_SESSION=XDEBUG_ECLIPSE; adbanner_city=%E4%B8%8A%E6%B5%B7%E5%B8%82; login_referer=https%3A%2F%2Fwww.epwk.com%2F; Hm_lpvt_387b8f4fdb89d4ea233922bdc6466394=1699021248; login_fail_need_graphics=0"
url = 'https://www.epwk.com/api/epwk/v1/user/login'

res = session.post(url=url, data=data)
print(res.text)
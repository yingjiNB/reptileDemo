# -- coding: utf-8 --
import requests
import json
url = 'https://mapi.yiche.com/web_api/car_model_api/api/v1/car/config_new_param'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "X-Platform": "pc"
}
params = {
    "cid": 508,
    "param": {"cityId": "2401", "serialId": "8278"}
}

json.loads()
res = requests.get(url=url, headers=headers, params=params)
print(res.text)
if __name__ == '__main__':
    pass

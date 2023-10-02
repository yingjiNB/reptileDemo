# -- coding: utf-8 --
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests

key = 'G$$QawckGfaLB97r'
iv = '9z6EtIbELlhpuN3e'
ming = '{"query":"python","cityCode":1,"industryCodes":"","pageNum":1,"limit":15}'

aes = AES.new(key=key.encode('utf-8'), mode=AES.MODE_CBC, iv=iv.encode('utf-8'))
mi = aes.encrypt(pad(ming.encode('utf-8'), 16))
mi = base64.b64encode(mi).decode().replace("/", "_").replace("+", "-").replace("=", "~")

params = {
    'b': mi,
    'kiv': iv
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

resp = requests.get(url="https://www.kanzhun.com/api_to/search/salary.json", params=params, headers=headers)
mi = resp.text

aes_dec = AES.new(key=key.encode('utf-8'), mode=AES.MODE_CBC, iv=iv.encode('utf-8'))
ming = aes_dec.decrypt(base64.b64decode(mi))
ming = unpad(ming,16)
ming = ming.decode('utf-8')
print(ming)

# print(mi)
if __name__ == '__main__':
    pass

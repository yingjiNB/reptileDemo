# -- coding: utf-8 --
import json
import base64
import requests
import ddddocr
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import settings

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
login_url = "https://user.wangxiao.cn/login?url=https%3A%2F%2Fwww.wangxiao.cn%2F"
session.get(url=login_url)
session.headers["Content-Type"] = "application/json; charset=utf-8"
# print(session.cookies)
# 获取图片验证码
verify_img_url = 'https://user.wangxiao.cn/apis//common/getImageCaptcha'
img_resp = session.post(url=verify_img_url)
img_resp_json = img_resp.json()
img_base64 = img_resp_json.get('data').split(',')[-1]
with open('./verify_img.png', mode='wb') as wf:
    wf.write(base64.b64decode(img_base64))
ocr = ddddocr.DdddOcr(show_ad=False)
# ocr.show_ad=False
verify_code = (ocr.classification(img_base64)).lower()
print(verify_code)

# 获取时间戳
get_time_resp = session.post(url='https://user.wangxiao.cn/apis//common/getTime')
get_time_resp_json = get_time_resp.json()
get_time = get_time_resp_json.get('data')

login_name = settings.login_name
password_ming = settings.password_ming

# 公钥处理成字节
rsa_key_bs = base64.b64decode(
    'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDA5Zq6ZdH/RMSvC8WKhp5gj6Ue4Lqjo0Q2PnyGbSkTlYku0HtVzbh3S9F9oHbxeO55E8tEEQ5wj/+52VMLavcuwkDypG66N6c1z0Fo2HgxV3e0tqt1wyNtmbwg7ruIYmFM+dErIpTiLRDvOy+0vgPcBVDfSUHwUSgUtIkyC47UNQIDAQAB')
# 加载公钥
pub_key = RSA.importKey(rsa_key_bs)
# 创建加密器
rsa = PKCS1_v1_5.new(pub_key)
password_mi_bs = rsa.encrypt((password_ming + '' + get_time).encode('utf-8'))
password_mi = base64.b64encode(password_mi_bs).decode()

login_url = 'https://user.wangxiao.cn/apis//login/passwordLogin'
login_data = {
    "imageCaptchaCode": verify_code,
    "password": password_mi,
    "userName": login_name
}
login_resp = session.post(url=login_url, data=json.dumps(login_data))
login_json = login_resp.json()
login_success_data = login_json.get('data')
session.cookies['autoLogin'] = 'null'
session.cookies['userInfo'] = json.dumps(login_success_data)
session.cookies['token'] = login_success_data.get('token')

session.cookies['UserCookieName'] = login_success_data.get('userName')
session.cookies['OldUsername2'] = login_success_data.get('userNameCookies')
session.cookies['OldUsername'] = login_success_data.get('userNameCookies')
session.cookies['OldPassword'] = login_success_data.get('passwordCookies')
session.cookies['UserCookieName_'] = login_success_data.get('userName')
session.cookies['OldUsername2_'] = login_success_data.get('userNameCookies')
session.cookies['OldUsername_'] = login_success_data.get('userNameCookies')
session.cookies['OldPassword_'] = login_success_data.get('passwordCookies')
session.cookies[login_success_data.get('userName') + '_exam'] = login_success_data.get('sign')

question_info = {"practiceType": "2",
                 "sign": "zj",
                 "subsign": "148c76abdb25324a5192",
                 "examPointType": "",
                 "questionType": "", "top": "30"}
question_resp = session.post(url='https://ks.wangxiao.cn/practice/listQuestions', data=json.dumps(question_info))
print(question_resp.text)

if __name__ == '__main__':
    pass

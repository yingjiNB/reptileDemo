import requests
from lxml import etree
from typing import List, Dict
import re


class GetFirstPPT:
    def __init__(self, url: str, headers: Dict[str, str]):
        self.url = url
        self.headers = headers
        self.site_url = "https://www.1ppt.com/moban/shengri/"
        self.folder_path = r".\birthday_ppt"

    def get_page_url(self):
        """获取分页链接"""
        response = requests.get(url=self.url, headers=self.headers)
        response.encoding = 'gbk'
        html = response.text
        # 得到最后一页
        last_page = re.search("<a href='ppt_shengri_(\d+).html'>末页</a>", html)
        page_url_list= [f"{self.url}ppt_shengri_{page}.html" for page in range(1,int(last_page.group(1))+1)]
        return page_url_list
if __name__ == '__main__':
    url = 'https://www.1ppt.com/moban/shengri/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    frist_ppt = GetFirstPPT(url=url, headers=headers)
    frist_ppt.get_page_url()

import requests
from lxml import etree
from typing import List, Dict
import re
import os

class GetFirstPPT:
    def __init__(self, url: str, headers: Dict[str, str]):
        self.url = url
        self.headers = headers
        self.site_url = "https://www.1ppt.com"
        self.folder_path = r".\birthday_ppt"

    def get_page_url(self):
        """获取分页链接"""
        response = requests.get(url=self.url, headers=self.headers)
        response.encoding = 'gbk'
        html = response.text
        # 得到最后一页
        last_page = re.search("<a href='ppt_shengri_(\d+).html'>末页</a>", html)
        page_url_list = [f"{self.url}ppt_shengri_{page}.html" for page in range(1, int(last_page.group(1)) + 1)]
        return page_url_list

    def get_image_url(self, page_url_list: List[str]):
        ppt_name_url_map:Dict[str,str] = {}
        for page_url in page_url_list:
            response = requests.get(url=page_url,headers=self.headers)
            response.encoding = 'gbk'
            html = etree.HTML(response.text)
            ppt_name_list = html.xpath('//dl[@class="dlbox"]//dd/ul[@class="tplist"]/li/h2/a/text()')
            ppt_img_url_list = html.xpath('//dl[@class="dlbox"]//dd/ul[@class="tplist"]/li/h2/a/@href')
            for ppt_name,ppt_img_url in zip(ppt_name_list,ppt_img_url_list):
                ppt_name_url_map[ppt_name] = self.site_url+ ppt_img_url

        return ppt_name_url_map
    def download_ppt(self,ppt_name_url_map:Dict[str,str]):
        # 判断文件夹是否存在没有就创建
        os.path.exists(self.folder_path) or os.makedirs(self.folder_path)
        for ppt_name,ppt_url in ppt_name_url_map.items():
            os.path.exists(self.folder_path+'\\'+ppt_name) or os.makedirs(self.folder_path+'\\'+ppt_name)

if __name__ == '__main__':
    url = 'https://www.1ppt.com/moban/shengri/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    frist_ppt = GetFirstPPT(url=url, headers=headers)
    # page_url_list = frist_ppt.get_page_url()
    page_url_list = ['https://www.1ppt.com/moban/shengri/ppt_shengri_1.html']
    ppt_name_url_map = frist_ppt.get_image_url(page_url_list)
    frist_ppt.download_ppt(ppt_name_url_map)

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
        ppt_name_url_map: Dict[str, str] = {}
        for page_url in page_url_list:
            response = requests.get(url=page_url, headers=self.headers)
            response.encoding = 'gbk'
            html = etree.HTML(response.text)
            ppt_name_list = html.xpath('//dl[@class="dlbox"]//dd/ul[@class="tplist"]/li/h2/a/text()')
            ppt_img_url_list = html.xpath('//dl[@class="dlbox"]//dd/ul[@class="tplist"]/li/h2/a/@href')
            for ppt_name, ppt_img_url in zip(ppt_name_list, ppt_img_url_list):
                ppt_name_url_map[ppt_name] = self.site_url + ppt_img_url
        print(ppt_name_url_map)
        return ppt_name_url_map

    def download_ppt(self, ppt_name_url_map: Dict[str, str]):
        # 判断文件夹是否存在没有就创建
        os.path.exists(self.folder_path) or os.makedirs(self.folder_path)
        for ppt_name, ppt_url in ppt_name_url_map.items():
            os.path.exists(self.folder_path + '\\' + ppt_name) or os.makedirs(self.folder_path + '\\' + ppt_name)
            # 获取图片文件
            response = requests.get(url=ppt_url, headers=self.headers)
            response.encoding = 'gbk'
            html = etree.HTML(response.text)
            img_url = html.xpath('//div[@class="content"]/p/img/@src')
            img1_file = requests.get(url=img_url[0], headers=self.headers)
            img2_file = requests.get(url=img_url[1], headers=self.headers)
            ppt_file_url = self.folder_path+r"\\"+ppt_name+r'\\'

            with open(f"{ppt_file_url}{img_url[0].split('/')[-1]}", mode='wb') as f:
                f.write(img1_file.content)
                print(f"{ppt_name}: 图片1下载成功")
            with open(f"{ppt_file_url}{img_url[1].split('/')[-1]}", mode='wb') as f:
                f.write(img2_file.content)
                print(f"{ppt_name}: 图片2下载成功")
            # 获取ppt文件
            ppt_url = html.xpath('//ul[@class="downurllist"]/li/a/@href')[0]
            ppt_url = self.site_url + ppt_url
            ppt_response = requests.get(url=ppt_url, headers=self.headers)
            ppt_response.encoding = 'gbk'
            ppt_html = etree.HTML(ppt_response.text)
            file_url = ppt_html.xpath('//li[@class="c1"]/a/@href')[0]
            ppt_file = requests.get(url=file_url,headers=headers)
            with open(f"{ppt_file_url}{file_url.split('/')[-1]}",mode='wb') as f:
                f.write(ppt_file.content)
                print(f"{ppt_name}:ppt文件下载成功")



if __name__ == '__main__':
    url = 'https://www.1ppt.com/moban/shengri/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    frist_ppt = GetFirstPPT(url=url, headers=headers)
    page_url_list = frist_ppt.get_page_url()
    # page_url_list = ['https://www.1ppt.com/moban/shengri/ppt_shengri_1.html']
    ppt_name_url_map = frist_ppt.get_image_url(page_url_list)
    # ppt_name_url_map = {'生日蛋糕背景的蓝色梦幻风生日快乐生日相册PPT模板': 'https://www.1ppt.com/article/97943.html'}
    frist_ppt.download_ppt(ppt_name_url_map)

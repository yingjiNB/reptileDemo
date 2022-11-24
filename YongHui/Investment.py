import requests
from lxml import etree
from typing import List, Dict
import os


class GetPeriodicReport:
    def __init__(self, url: str, headers: Dict[str, str]):
        self.url = url
        self.headers = headers
        self.site_url = "http://www.yonghui.com.cn"
        self.folder_path = r".\report_file"

    def get_page_url(self) -> List[str]:
        # 获取分页链接
        response: str = requests.get(url=self.url, headers=self.headers).text
        html = etree.HTML(response)
        num_page_list: List[str] = html.xpath('//div[@class="numPage"]//a/text()')
        num_page_list.pop(0)
        page_url_list: List[str] = [self.url + f'&p={num_page}' for num_page in num_page_list]
        return page_url_list

    def get_report_url(self, page_url_list: List[str]) -> Dict[str, str]:
        report_url_all_dict: Dict[str, str] = {}
        for page_url in page_url_list:
            response = requests.get(url=page_url, headers=self.headers).text
            html = etree.HTML(response)
            date_lsit = html.xpath('//div[@id="divlist"]/li/a/h1/text()')
            name_lsit = html.xpath('//div[@id="divlist"]/li/a/h2/text()')
            report_name_list = [f"{report_data}-{report_name}" for report_data, report_name in
                                zip(date_lsit, name_lsit)]
            report_href_list = html.xpath('//div[@id="divlist"]/li/a/@href')
            # print(report_href_list)
            report_url_list = [f"{self.site_url}{report_href}" if self.site_url not in report_href else report_href for
                               report_href in report_href_list]

            for report_name, report_url in zip(report_name_list, report_url_list):
                report_url_all_dict[report_name] = report_url

        return report_url_all_dict

    def download_report_file(self, report_url_dict: Dict[str, str], ):
        # 判断文件夹是否存在没有就创建
        os.path.exists(self.folder_path) or os.makedirs(self.folder_path)
        for report_name,report_url in report_url_dict.items():
            response = requests.get(url=report_url,headers=self.headers)
            report_file_url = self.folder_path+r"\\"+report_name+".PDF"
            with open(report_file_url,mode='wb') as f:
                f.write(response.content)
                print(f'{report_name}下载成功')


if __name__ == '__main__':
    url = 'https://www.yonghui.com.cn/inv?ctlgid=654114'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    yonghui_report = GetPeriodicReport(url=url, headers=headers)
    page_url_list: List[str] = yonghui_report.get_page_url()

    report_url_dict = yonghui_report.get_report_url(page_url_list)
    yonghui_report.download_report_file(report_url_dict)

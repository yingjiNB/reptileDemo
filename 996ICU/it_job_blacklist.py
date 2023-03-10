# -- coding: utf-8 --
import time

import aiohttp
import aiomysql
import asyncio

import requests
import pymysql
import toml
from lxml import etree
from faker import Factory


# class ITBlank:
#     def __init__(self, ):
#         self.headers = {'user-agent': Factory.create().user_agent()}
#         self.config = toml.load('secre_config.toml')
#
#     async def get_url(self, url, semaphore):
#         print(url)
#         # 公司名称  详细描述  城市（详情）  ID（详情） 回复ID（详情）
#         async with semaphore:
#             async with aiohttp.ClientSession() as session:
#                 async with await session.get(url=url, headers=self.headers, ) as res:
#                     response = await res.text()
#                     html = etree.HTML(response)
#                     # 详情链接
#                     detail_urls = html.xpath(f'//div[@id="main"]//a[@itemprop="url"]/@href')
#                     print(detail_urls)
#                     tasks = [asyncio.ensure_future(self.get_detail(detail_url)) for detail_url in detail_urls]
#                     response_task = await asyncio.gather(*tasks)
#                     return response_task
#     async def get_detail(self, detail_url: str):
#         # print(detail_url)
#         semaphore = asyncio.Semaphore(1)
#         async with semaphore:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url=detail_url, headers=self.headers) as res:
#                     response = await res.text()
#                     html = etree.HTML(response)
#                     # # 公司名称
#                     company_name = html.xpath(f'//div[@class="row"]//h1/text()')[0]
#
#                     # 详情描述
#                     detail_desc = html.xpath(f'//div[@class="post-content"]//blockquote[2]/p/text()')
#                     # 城市
#                     city = html.xpath('//div[@class="post-content"]//blockquote[4]/p/text()')
#                     # 详情ID
#                     detail_id = detail_url.split('/')[-2]
#                     # 回复ID
#                     # comment_id = html.xpath(f'//div[@class="info"]/ul/li//form/@action')[0].split('=')[-1]
#                     comment_id = html.xpath(f'//div[@class="info"]/ul/li//form/@action')
#                     print(detail_url, company_name, comment_id)
#                     await asyncio.sleep(2)
#                     # await self.save_data(str(company_name), str(detail_desc), str(city), str(detail_id), comment_id)
#
#     async def save_data(self, company_name, detail_desc, city, detail_id, comment_id):
#         conn = await aiomysql.connect(host=self.config['database']['host'], port=self.config['database']['port'],
#                                       user=self.config['database']['username'],
#                                       password=self.config['database']['password'], db=self.config['database']['db'],
#                                       charset='utf8mb4', cursorclass=aiomysql.cursors.DictCursor)
#         async with conn.cursor() as cursor:
#             await cursor.execute(
#                 "INSERT INTO it_black (company_name, detail_desc, city, detail_id, comment_id) VALUES (%s, %s, %s, %s, %s)",
#                 (company_name, detail_desc, city, detail_id, comment_id))
#             await conn.commit()
#         conn.close()

class ITBlank():
    def __init__(self, ):
        self.headers = {'user-agent': Factory.create().user_agent()}
        self.config = toml.load('secre_config.toml')
        self.conn = pymysql.connect(host=self.config['database']['host'], port=self.config['database']['port'],
                                    user=self.config['database']['username'],
                                    password=self.config['database']['password'],
                                    database=self.config['database']['db'],
                                    charset='utf8mb4', )
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_url(self, url, ):
        # 公司名称  详细描述  城市（详情）  ID（详情） 回复ID（详情）
        response = requests.get(url=url, headers=self.headers).text
        html = etree.HTML(response)
        # 详情链接
        detail_urls = html.xpath(f'//div[@id="main"]//a[@itemprop="url"]/@href')

        for detail_url in detail_urls:
            print(detail_url)
            self.get_detail_url(detail_url)

    def get_detail_url(self, detail_url):
        response = requests.get(url=detail_url, headers=self.headers).text
        html = etree.HTML(response)
        # 公司名称
        company_name = html.xpath(f'//div[@class="row"]//h1/text()')[0]
        # 详情描述
        detail_desc = html.xpath(f'//div[@class="post-content"]//blockquote[2]/p/text()')
        # 城市
        city = html.xpath('//div[@class="post-content"]//blockquote[4]/p/text()')
        # 详情ID
        detail_id = detail_url.split('/')[-2]
        # 回复ID
        comment_id = html.xpath(f'//div[@class="info"]/ul/li//form/@action')[0].split('=')[-1]
        self.save_data(str(company_name), str(detail_desc), str(city), str(detail_id), comment_id)

    def save_data(self, company_name, detail_desc, city, detail_id, comment_id):

        self.cursor.execute('''
            INSERT INTO it_black (company_name,detail_desc,city,detail_id,comment_id) 
            VALUES (%s, %s, %s, %s, %s);
        ''', (company_name, detail_desc, city, detail_id, comment_id))
        self.conn.commit()
        print(f"{company_name}插入成功")


if __name__ == '__main__':
    # urls = [f'https://job.me88.top/index.php/page/{i}/' for i in range(1, 45)]
    # it_blank = ITBlank()
    # semaphore = asyncio.Semaphore(1)
    # loop = asyncio.get_event_loop()
    # tasks = [asyncio.ensure_future(it_blank.get_url(url, semaphore)) for url in urls]
    # tasks = asyncio.gather(*tasks)
    # loop.run_until_complete(tasks)
    # loop.close()

    it_blank = ITBlank()
    for i in range(2, 45):
        print(f'第{i}页开始')
        url = f'https://job.me88.top/index.php/page/{i}/'
        it_blank.get_url(url=url)
        print(f'第{i}页完成')
        time.sleep(0.5)

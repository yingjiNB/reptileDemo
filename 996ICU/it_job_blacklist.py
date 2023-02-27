# -- coding: utf-8 --

import aiohttp
import aiofiles
import asyncio
from asgiref.sync import sync_to_async
from lxml import etree
from faker import Factory


class ITBlank:
    def __init__(self, ):
        self.headers = {'user-agent': Factory.create().user_agent()}

    async def get_url(self, url):
        # 公司名称  详细描述  城市（详情）  ID（详情） 回复ID（详情）
        async with aiohttp.ClientSession() as session:
            async with await session.get(url=url, headers=self.headers) as res:
                response = await res.text()
                html = etree.HTML(response)
                # 详情链接
                # detail_urls = html.xpath(f'//div[@id="main"]//a[@itemprop="url"]/@href')
                detail_urls = ['https://job.me88.top/index.php/archives/21654/']

                tasks = [asyncio.ensure_future(self.get_detail(detail_url)) for detail_url in detail_urls]
                response_task = await asyncio.gather(*tasks)
                return response_task

    async def get_detail(self, detail_url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=detail_url, headers=self.headers) as res:
                response = await res.text()

                html = etree.HTML(response)
                # 公司名称
                company_name = html.xpath(f'//div[@class="row"]//h1[@class="post-title"]/text()')[0]
                # 详情描述
                detail_desc = html.xpath(f'//div[@class="post-content"]//blockquote[2]/p/text()')
                city = html.xpath('//div[@class="post-content"]//blockquote[4]/p/text()')
                # 详情ID
                detail_id = detail_url.split('/')[-2]
                comment_id = html.xpath(f'//div[@class="info"]/ul/li//form/@action')[0].split('=')[-1]
                print(company_name)
                print(detail_desc)
                print(city)
                print(detail_id)
                print(comment_id)


if __name__ == '__main__':
    urls = [f'https://job.me88.top/index.php/page/{i}/' for i in range(1, 2)]
    it_blank = ITBlank()
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(it_blank.get_url(url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
    # loop.close()

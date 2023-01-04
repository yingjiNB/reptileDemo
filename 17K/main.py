# -- coding: utf-8 --
import os

import aiohttp
import asyncio
from lxml import etree
from faker import Factory


async def data_analysis(url, headers):
    async with aiohttp.ClientSession() as session:
        async with await session.get(url=url, headers=headers) as res:
            res_obj = await res.text()
            # print(res_obj)
            html = etree.HTML(res_obj)
            # 获取卷名称
            volumes = html.xpath('//dl[@class="Volume"]/dt/span[1]/text()')
            # 获取卷名称更新信息
            volumes_info = html.xpath('//dl[@class="Volume"]/dt/span[2]/text()')
            volumes_list = (volumes[i] + '-' + volumes_info[i] for i in range(0, len(volumes)))
            for volume in volumes_list:
                volume_path = r".\file\\" + volume + '\\'
                os.path.exists(volume_path) or os.makedirs(volume_path)
            for i in range(0, len(volumes)):
                # 获取章节名称
                chapters = html.xpath()


if __name__ == '__main__':
    url = 'https://www.17k.com/list/493239.html'
    ua = Factory.create().user_agent()
    headers = {
        'user-agent': ua
    }
    # asyncio.run(data_analysis(url, headers))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(data_analysis(url, headers))

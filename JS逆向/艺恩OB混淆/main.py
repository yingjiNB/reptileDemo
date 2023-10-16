# -- coding: utf-8 --

import asyncio
# import aiohttp
from typing import List, Dict

import aiofiles

from aiohttp import ClientSession
import subprocess  # 执行命令行的
from functools import partial  # 固定某个参数的

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

import execjs


async def fetch_data_with_post(params, session):
    params['MethodName'] = 'BoxOffice_GetYearInfoData'
    url = 'https://www.endata.com.cn/API/GetData.ashx'  # 假设这是固定的URL
    async with session.post(url, data=params) as response:
        print('当前年份', params['year'])
        return {params['year']: await response.text()}


async def aio_download(year, result):
    file_name = f'{year}年度票房'
    async with aiofiles.open(f'{file_name}.json', 'w', encoding='utf-8') as f:
        await f.write(result)
        print(f'{file_name}下载完成')


async def main():
    start_year = 2008
    end_year = 2023
    params_list = [{'year': year} for year in range(start_year, end_year + 1)]

    async with ClientSession() as session:
        tasks = [fetch_data_with_post(params, session) for params in params_list]
        results: [List[Dict[str:str]]] = await asyncio.gather(*tasks)
        async with aiofiles.open('webDES2.js', mode='r', encoding='utf-8') as r_f:
            js_code = await r_f.read()
        js = execjs.compile(js_code)
        tasks = []
        for result in results:
            for year, data in result.items():
                ret = js.call('fn', data)
                tasks.append(aio_download(year, ret))
        await asyncio.wait(tasks)
        # write_tasks = [aio_download(year, js.call('fn', data)) for result in results for year, data in result.items()]
        # await asyncio.gather(*write_tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

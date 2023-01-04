# -- coding: utf-8 --
import aiohttp
import asyncio


async def data_analysis(url, headers):
    async with aiohttp.ClientSession() as session:
        async with await session.get(url=url, headers=headers) as res:
            print(await res.text())


if __name__ == '__main__':
    url = 'https://www.17k.com/book/493239.html'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    # asyncio.run(data_analysis(url, headers))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(data_analysis(url, headers))
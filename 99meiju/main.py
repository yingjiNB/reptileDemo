# -- coding: utf-8 --
import asyncio
import aiohttp
from aiohttp import TCPConnector
import aiofiles
from faker import Factory
import re
import os


async def get_m3u8_url(url: str):
    '''
    抓取页面中的index.m3u8的文件数据 写入到本地index.m3u8文件并返回m3u8url地址
    :param url: 页面的url（要抓取的视频的页面url）
    :return: url
    '''
    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False), headers=headers) as session:
        async with await session.get(url) as resp:
            data = await resp.text(encoding='UTF-8')
            # # 获取m3u8链接
            first_index_m3u8_url = re.search('var now="(.*?)"', data).group(1).replace('\\', '')
            async with await session.get(first_index_m3u8_url) as resp:
                data = await resp.text(encoding='UTF-8')
                # print(data)
                second_url = data.split('\n')[-2]

                second_url_index_m3u8_url = first_index_m3u8_url.rsplit('/', 1)[0] + '/' + second_url.split('/', 3)[-1]
                # print(second_url_index_m3u8_url)
                async with await session.get(second_url_index_m3u8_url) as resp:
                    data = await resp.text(encoding='UTF-8')
                    async with aiofiles.open('index.m3u8', 'w', encoding='UTF-8') as f:
                        await f.write(data)
        # 返回截取ts文件需要的前半部分的url

        return first_index_m3u8_url.rsplit('/', 3)[0]


async def download_all_m3u8(path: str, url: str, filename='index.m3u8'):
    '''
    下载所有的m3u8的里面的ts文件
    :param path: 存储下载ts文件的文件夹
    :param filename: m3u8的文件名称
    :re
    '''
    with open(filename, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    # 判断 当前存储ts的文件目录是否存在 不存在则创建
    if not os.path.exists(path):
        os.mkdir(path)
    # 创建信号量 并发下载
    sem = asyncio.Semaphore(100)
    tasks = []
    # 循环读取每一行数据
    i = 0
    for line in lines:
        # 获取所有要下载的ts的url地址  不以#作为开头
        if line.startswith('#'):
            continue
        # 进行下载处理
        ts_url = url + '/' + line.strip()  # 去除请求的url中可能包含的其他的字符
        tasks.append(asyncio.create_task(dowload_one_m3u8(ts_url, i, path, sem)))
        i += 1
    # 集体等待
    await asyncio.wait(tasks)


async def dowload_one_m3u8(url, i, path, sem):
    '''
    下载单个ts文件的函数
    :param url: 要下载ts的url地址
    :param i: 当前的文件的名称  也就是i的循环自增
    :param path: 当前下载后ts所需要存储的路径
    :return:
    '''
    while True:
        # 使用信号量 控制并发
        async with sem:
            try:
                async with aiohttp.ClientSession(connector=TCPConnector(ssl=False), headers=headers) as session:
                    print(url, '正在下载')
                    async with session.get(url, timeout=60) as resp:
                        data = await resp.read()
                        # 拼接下载文件的路径及下载后ts的文件名称
                        file_path = os.path.join(path, str(i) + '.ts')
                        # 进行下载写入
                        async with aiofiles.open(file_path, 'wb') as f:
                            await f.write(data)
                            print(url, '下载成功~')
                            break
            except:
                print(url, '请求超时~ 重新下载中')


def do_index_m3u8(path, url,filename='index.m3u8',):
    '''
    将index.m3u8写入到ts文件夹内 将ts url改名为 0.ts 1.ts  目的是为了和ts文件中的ts文件进行对象
    '''
    with open(filename, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    # 判断 当前存储ts的文件目录是否存在 不存在则创建
    if not os.path.exists(path):
        os.mkdir(path)
    file_path = os.path.join(path, filename)
    print(file_path)
    f = open(file_path, 'w', encoding='UTF-8')


    i = 0
    for line in lines:
        # 获取所有要下载的ts的url地址  不以#作为开头
        if line.startswith('#'):
            # 判断处理是存在需要秘钥
            if line.find('URI') != -1:
                line = re.sub(r'(#EXT-X-KEY:METHOD=AES-128,URI=")(.*?)"', r'D:\\Project\\reptileDemo\\99meiju\\ts\\key.m3u8"',line)
                print(line)
                host = url[0] + '/20220514/oNsna1im/1200kb/hls'
                line = f"#EXT-X-KEY:METHOD=AES-128,URI="+'\"'+line+'\"'
                # 爬取key
                download_m3u8(host + '/key.key', os.path.join(path, 'key.m3u8'))
            f.write(line)
        else:
            f.write(str(i) + '.ts\n')
            i += 1


def download_m3u8(url, m3u8_filename="index.m3u8", state=0):
    import requests
    print('正在下载index.m3u8文件')
    resp = requests.get(url, headers=headers)
    with open(m3u8_filename, mode="w", encoding="utf-8") as f:
        f.write(resp.text)


def merge(path, filename='output'):
    '''
    进行ts文件合并 解决视频音频不同步的问题 建议使用这种
    :param filePath:
    :return:
    '''
    os.chdir(path)  # 进入到ts文件夹 然后执行下面的命令
    cmd = f'ffmpeg -i index.m3u8 -c copy {filename}.mp4'
    os.system(cmd)


async def main(url, path):
    # task = asyncio.create_task(get_m3u8_url(url))
    # url = await asyncio.gather(task)
    # task = asyncio.create_task(download_all_m3u8(path, url[0]))
    # await asyncio.gather(task)
    # do_index_m3u8(path,url)  # 处理index.m3u8文件
    merge(path, '拜托了')  # 合并视频


if __name__ == '__main__':
    url = 'https://www.99meijutt.com/play/15009-2-0.html'
    ua = Factory.create().user_agent()
    headers = {
        'user-agent': ua
    }
    path = 'ts'
    # asyncio.run(main(url, path))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url, path))

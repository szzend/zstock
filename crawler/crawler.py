#coding: utf-8
"""
此模块实现爬取，调度及辅助工具

"""
import asyncio 
from aiohttp import ClientSession,ServerTimeoutError
import random
import multiprocessing
import os
from .logger import Logger
from .settings import Settings


http_agent=[
    {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:58.0) Gecko/20100101 Firefox/58.0'
    },
    {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        #'Referer': 'http://vip.stock.finance.sina.com.cn/mkt/',
        'Content-type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive'
    },
    {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
    }
]
__logger__=Logger()

def getlog():
    return __logger__

class Crawler:
    """
    实现调度及行为控制
    """
    def __init__(self):
        self.read_timeout=5.0
        self.conn_timeout=2.0
        self.agent=None
        self.proxy_pool=None
        self.client=None
        

    def make_config(self, use_agent=False,use_proxy=False,agent=None,proxy_pool=[]):
        """
        参数:   use_agent 参数类型为布尔，指定是否设置请求头
                use_proxy 参数类型为布尔，指定是否使用代理服务器
                agent 参数类型为字典或字典列表，设置请求头，为字典列表时每次请求随机使用
                proxy_pool参数类型为列表，指定将使用的代理池
        """
        if use_agent:
            if agent:
                if isinstance(agent,dict):
                    self.agent=list(agent)
            else:
                self.agent=http_agent
        if use_proxy:
            self.proxy_pool=proxy_pool

    def __add_urls(self,urls):
        pass
    def __add_item(self,item):
        pass
    async def __fetch(self,client,url,headers=None,proxy=None):
        print('from __fetch..')
        try:
            async with client.get(url,headers=headers,proxy=proxy) as response:
                #return await response.text()
                getlog().info(str(response))
                return response
        except ServerTimeoutError as err:
            getlog().error(str(err))
    async def __request(self,client,url):
        headers=random.choice(self.agent) if self.agent else None
        #print(headers)
        proxy=random.choice(self.proxy_pool) if self.proxy_pool else None
        #限制并发数
        LIMIT_REQUESTS=100
        async with asyncio.Semaphore(LIMIT_REQUESTS):
            html=await self.__fetch(client,url,headers=headers,proxy=proxy)
            results=await asyncio.gather(asyncio.ensure_future(self.__spider.process_links(html)),
            asyncio.ensure_future(self.__spider.parse_item(html)))
            self.__add_urls(results[0])
            self.__add_item(results[1])

        

    async def __work(self,urls):
        async with ClientSession(read_timeout=self.read_timeout,conn_timeout=self.conn_timeout) as client:
            tasks=[asyncio.ensure_future(self.__request(client,url)) for url in urls]
            return await asyncio.gather(*tasks)

    async def __dispatch(self,use_mulp=True):
        urls=await self.__spider.start_urls()
        urls=list(set(urls+self.__spider.urls))
        num=len(urls)
        print(urls)
        threshold=100   #阈值，超过此任务数则开启多进程
        if use_mulp and num>threshold:
            count=multiprocessing.cpu_count()
            p = multiprocessing.Pool()
            for i in range(count):
                _=urls[i*num//count:(i+1)*num//count]
                p.apply_async(self.start,(_,),)     #此处参数传值注意
            p.close()
            p.join()
        else:
            await self.__work(urls)
    def start(self,urls,spider=None):
        if not spider:
            print(os.getpid())
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            print(loop)
            print(loop.__hash__())
            loop.run_until_complete(self.__work(urls))
            loop.run_until_complete(asyncio.sleep(0))
            loop.close() 
        else:
            self.run(spider)

    def run(self,spider,use_mulp=True,debug=False):
        self.__spider=spider
        loop = asyncio.get_event_loop()
        getlog().debug=debug
        getlog().start()
        loop.run_until_complete(self.__dispatch(use_mulp))
        loop.run_until_complete(asyncio.sleep(0))
        #loop.close()
        getlog().stop()
        print(getlog().report())

#coding: utf-8
"""
此模块实现爬取，调度及辅助工具
"""
import asyncio 
from aiohttp import ClientSession
import random

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

class Crawler:
    """
    实现调度及行为控制
    """
    def __init__(self,spider):
        self.spider=spider
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


    async def __fetch(self,url,headers=None,proxy=None):
        async with self.client.get(url,headers=headers,proxy=proxy) as response:
            return await response.text()

    async def __work(self,url):
        headers=random.choice(self.agent) if self.agent else None
        proxy=random.choice(self.proxy_pool) if self.proxy_pool else None
        html=await self.__fetch(url,headers=headers,proxy=proxy)
        result=await self.spider.parse(html)

    def run(self):
        self.client=ClientSession(read_timeout=self.read_timeout,conn_timeout=self.conn_timeout)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__work(self.spider.urls[0]))
        loop.run_until_complete(asyncio.sleep(0))
        loop.close()
        self.client.close()

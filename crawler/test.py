from .parser import HtmlParser
from .crawler import Crawler
import asyncio
import os
class  mySpider(HtmlParser):
    async def parse_item(self,response):
        print(f"ready to print response:{os.getpid()}")
        return response
        
    async def process_links(self,response):
        print(f"process_links,before ..{os.getpid()}")
        await asyncio.sleep(5)
        print(f"process_links,back..{os.getpid()}")
        return ['http://result']

    async def start_urls(self):
        urls=['https://baidu.com','http://www.sohu.com/']
        return urls
def make_urls(s:mySpider,n:int):
    u='https://www.baidu.com/s?wd='
    urls=[u+str(i+1) for i in range(n)]
    s.urls=urls

s=mySpider()
c=Crawler()
c.make_config(use_agent=True)


def start2():
    s=mySpider()
    c=Crawler()
    c.make_config(use_agent=True)
    c.run(s,False)
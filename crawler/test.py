from .spider import HtmlSpider
from .crawler import Crawler
import asyncio
import os
class  mySpider(HtmlSpider):
    async def parse_item(self,response):
        print(f"ready to print response:{os.getpid()}")
        await asyncio.sleep(2)
        print(os.getpid(),response)
        
    async def process_links(self,response):
        print(f"process_links,before ..{os.getpid()}")
        await asyncio.sleep(5)
        print(f"process_links,back..{os.getpid()}")
        return ['http://result']

    async def start_urls(self):
        urls=['https://baidu.com','http://www.sohu.com/']
        return urls*60


def start():
    s=mySpider()
    c=Crawler()
    c.run(s)
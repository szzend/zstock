from .spider import HtmlSpider
from .crawler import Crawler
import asyncio
class  mySpider(HtmlSpider):
    async def parse_item(self,response):
        print("ready to print response")
        await asyncio.sleep(2)
        print(response)
        
    async def process_links(self,response):
        print("process_links,before ..")
        await asyncio.sleep(5)
        print("process_links,back..")
        return ['http://result']

    async def start_urls(self):
        urls=['https://baidu.com','http://www.sohu.com/']
        return urls*60


def start():
    s=mySpider()
    c=Crawler()
    c.run(s)
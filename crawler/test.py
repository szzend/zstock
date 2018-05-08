from .spider import HtmlSpider
from .crawler import Crawler

class  mySpider(HtmlSpider):
    def parse(self,response):
        print(response)


def start():
    s=mySpider(['https://baidu.com'])
    c=Crawler(s)
    c.run()
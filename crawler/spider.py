#coding: utf-8
"""
此模块用于提取分析
"""

class Spider:
    """
    用于爬虫基类
    """
    pass

class HtmlSpider(Spider):
    """
    主要用于静态内容页提取，包括html,xml,json
    

    """
    def __init__(self,start_urls=[]):
        self.__urls=start_urls
        
        
    @property
    def urls(self):
        return self.__urls

    @urls.setter
    def urls(self,value):
        self.__urls=value

        
    
    async def start_urls(self):
        """
        生成要抓取的urls,
        用于向crawler提供初始请求的urls
        返回：urls列表
        """
        return self.urls

    async def process_links(self,response):
        """
        被crawler调用，用于提取并处理页面中的urls
        返回：需要被crawler处理的urls列表
        """
        pass


    async def parse_item(self,response):
        """
        被crawler调用，用于提取需要的内容
        返回：任意对象
        """
        raise NotImplementedError

    
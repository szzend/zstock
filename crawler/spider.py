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
    def __init__(self,urls=[]):
        self.urls=urls
        self.pipeline=[]

    @property
    def urls(self):
        return self.__urls

    @urls.setter
    def urls(self,value):
        """
        value必须为列表
        """
        try:
            self.__urls=list(set(self.make_urls()+value))
        except NotImplementedError:
            self.__urls=value
    
    def make_urls(self):
        """
        用于生成要分析的urls,此方法非必须，
        如果提供则与初始化时提供的开始urls合并
        返回：urls列表
        """
        raise NotImplementedError

    def extract(self,response):
        """
        用于提取需要继续爬取的url
        返回：url列表或空
        """
        raise NotImplementedError
    
    def parse(self,response):
        """
        用于提取内容
        返回：任意对象
        """
        raise NotImplementedError

    def add_pipeline(self,pipe):
        """
        添加pipe对象到处理管线
        """
        self.pipeline.append(pipe)
#coding: utf-8
"""
此模块用于提取分析
"""

class Parser:
    """
    用于分析器基类
    """
    def __init__(self,start_urls=[]):
        self.__urls=start_urls
        self.__done=False   #标识爬行是否完成, 当爬行完成后由crawler设置为True
        self.__result=None  #保存本次爬行情况的结果(非抓取的数据结果,抓取的数据由使用者自行处理,)

    @property
    def done(self):
        return self.__done
        
    @property
    def result(self):
        return self.__result

    @property
    def urls(self):
        return self.__urls

    @urls.setter
    def urls(self,value):
        self.__urls=value
        self.__done=False

    
    def callback_done(self,result):
        self.__done=True
        self.__result=result

class HtmlParser(Parser):
    """
    主要用于静态内容页提取，包括html,xml,json
    
    """
  
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
        pass

    
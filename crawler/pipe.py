#coding: utf-8
class pipe:
    """
    用于pipeline处理数据
    """
    def process(self,item):
        """
        处理数据的函数，必须实现此方法
        参数：item 为待处理的数据
        返回：需要继续处理的数据或空
        """
        raise NotImplementedError
#coding=utf-8

"""
此包用于获取股票数据
公用接口在interface
"""
import time
from requests import Session
from requests.adapters import HTTPAdapter

__all__=[]


stockwords={
        'date':'日期', 'tdate':'日期','time':'时间','ticktime':'时间', 'tdatetime':'日期时间','price':'成交价格','trade':'成交价格',
        'volume':'成交量(股)','amount':'成交额(元)','pb':'市净率','mktcap':'总市值(万元)',
        'nmc':'流通市值(万元)','turnoverratio':'换手率','pricechange':'价格变动','buy':'现买价',
        'sell':'现卖价','code':'股票代码','name':'名称','open':'开盘','close':'收盘','high':'最高',
        'low':'最低','settlement':'昨日收盘','changepercent':'变动比','factor':'复权因子',
        'qt':'数量(股)','bs':'内外盘'
}

def w2d(words,dic=stockwords,u='unknown'):
        """
        返回新的列表(描述相应键)
        参数：words:为字符串列表
              dic:为字典
              u:string 未找到键时的返回值
        返回：根据words中的字符串值返回字典对应中的值，未找到的键返回’未知’
        """
        return [dic.get(k,u) for k in words]

def id2code(id,type):
        """
        根据股票ID转换为各接口需要的格式
        0,3开头为深圳市场,6开头为上海市场
        参数：id:string(形如000100,600100,300100)
              type:{0,1,2}(0不变,1增加前缀,2增加后缀)
        返回：string(转换后的股票代码)
        """
        r={
                '00':lambda:id,
                '03':lambda:id,
                '06':lambda:id,
                '10':lambda:'sz'+id,
                '13':lambda:'sz'+id,
                '16':lambda:'sh'+id,
                '20':lambda:id+'2',
                '23':lambda:id+'2',
                '26':lambda:id+'1'
        }.get(str(type)+id[0],lambda:None)()
        if not r:
                raise ValueError('({0},{1})非预期转换.'.format(id,type))
        return r

class grasp():
        """
        封装requests会话类,用于处理超时及抓取频率
        """
        def __init__(self,max_retries=3,useproxy=False):
                self.__session=Session()
                self.__session.mount('http://',HTTPAdapter(max_retries=max_retries))
                self.__session.mount('https://',HTTPAdapter(max_retries=max_retries))
        
        def get(self,url,timeout=0.2,interval=0.03,**kwargs):
                time.sleep(interval)
                r=self.__session.get(url,timeout=(timeout,15),**kwargs)
                #print(r)
                #print(r.url)
                return r
        

        def close(self):
                self.__session.close()



#用于模拟浏览器
_headers1={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:58.0) Gecko/20100101 Firefox/58.0'
}
_headers2={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
_headers3={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        #'Referer': 'http://vip.stock.finance.sina.com.cn/mkt/',
        'Content-type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive'
}
_headers4={
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
}
headers=[_headers1,_headers2,_headers3,_headers4]
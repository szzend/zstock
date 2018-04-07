#coding=utf-8
"""
用于构建代理池
"""
from multiprocessing import Pool,Queue
import pandas as pd
from io import BytesIO
from lxml import etree
from requests import Session
from requests.adapters import HTTPAdapter
import random
from .import headers

class proxypool():
    """
    """

    #66源
    #__url6='http://www.66ip.cn/{area}/1.html'
    

    def __init__(self,max_retries=3):
        self.__session=Session()
        self.__session.mount('http://',HTTPAdapter(max_retries=max_retries))
        self.__session.mount('https://',HTTPAdapter(max_retries=max_retries))
        self.__untestpool=set()
        self.__badpool=set()
        self.__pool=set()

    def test(self):
        def t(p):
            """
            返回结果元组,第一位为1或0,1代表可用,0代表不可用;第二位为协议及IP
            """
            #self.__session.get()


        lt=list(self.__untestpool-self.__pool-self.__badpool)
        result=[]
        with Pool() as pool:
            result=[pool.apply_async(t,(p,)) for p in lt] 
            result=[r.get() for r in result]
        for r in result:
            b,p=r
            if b:
                self.__pool.add(p)
            else:
                self.__badpool.add(p)


    def buildxc(self):
        #西刺源,抓取前7页
        result=[]
        pool=set()
        for p in range(1,8):
            url='http://www.xicidaili.com/nn/{p}'.format(p=p)
            r=self.__session.get(url,timeout=(2,15),headers=random.choice(headers))
            r.encoding='utf-8'
            html = etree.HTML(r.text)
            tb = html.xpath('//table[@id="ip_list"]')
            dfs=pd.read_html(etree.tostring(tb[0]),header=0,flavor='lxml')
            result.append(dfs[0])
        result=pd.concat(result)[['类型','IP地址','端口']].values
        for lt in result:
            pool.add('{}://{}:{}'.format(lt[0].lower(),lt[1],lt[2]))
        self.__untestpool=self.__untestpool.union(pool)
        return self.__untestpool        
        
  

    def refresh(self):
        pass

    @property
    def pool(self):
        pass
    
    def __fetch(self):
        pass

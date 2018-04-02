#coding=utf-8
'''
腾讯股票网页数据获取接口
'''
import pandas as pd
import requests
import re
from io import BytesIO
from . import id2code,grasp


def tt_get_MX_x(stockid,date):
    '''
    从腾讯网页下载股票分笔明细数据Excel并读入DataFrame
    参数:   stockid:string(股票代码，如000038)
            date:string(交易日期，格式：yyyymmdd,如20180308)
    返回：  返回DataFrame(该数据包含列为:['成交时间','成交价格','成交量(手)','成交额(元)','性质'])
    '''
    #结果为excel表(实际格式为csv格式)，symbol形如sz000038,date形如20180308
    _URL='http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c={symbol}&d={date}'
    #用于异常返回信息
    _msg1='{}({},{})执行结果错误:{}'
    _msg2='{}({},{})执行结果错误,数据结构已改变,要求列为:{}'
    _names=['成交时间','成交价格','成交量(手)','成交额(元)','性质']
    _columns=['time','price','volume','amount','bs']
    url=_URL.format(symbol=id2code(stockid,1),date=date)
    #原始列为:成交时间	成交价格	价格变动	成交量(手)	成交额(元)	性质
    #选择列读入
    try:
        g=grasp()
        r=g.get(url)
        assert r.ok
        df=pd.read_table(BytesIO(r.content),sep='\t',usecols=[0,1,3,4,5],encoding='gbk')
    except ValueError as err:
        print(stockid,date,url,err)
        #raise ValueError(_msg1.format(tt_get_MX_x.__name__,stockid,date,str(err))) from err
    if list(df.columns)==_names:
        df.columns=_columns
        return df
    else:
        return None
        #raise ValueError(_msg2.format(tt_get_MX_x.__name__,stockid,date,str(_names)))



def tt_get_trade(stockid):
    """
    获取实时交易数据
    参数:
    返回:
    """
    #symbol形如sz000068,sh600188,返回以下栏位及分时明细
    _URL='http://web.sqt.gtimg.cn/q={symbol}'
    _columns=['现价','昨收','开盘','成交量(手)','外盘(手)','内盘(手)']
    raise NotImplementedError('数据不实用，未实现此方法')

def tt_get_MX_w(stockid,tail=None):
    """
    获取实时成交明细数据
    参数:stockid(string):股票id
        tail(int) 如为空或零则返回所有数据, 
        如为正数则返回最近的tail个时间段数据
        如为负数则返回最先的tail个时间段数据
    返回:DataFrame，coulumn=[索引，时间，价格，价格变动，成交量，成交额，内外盘]
    """
    #获取已有时间段,c形如sh600000,sz000068
    _cURL='http://stock.gtimg.cn/data/index.php?appn=detail&action=timeline&c={c}'
    #获取成交明细数据(按时间段分页)c形如sh600000,sz000068,p为页码(70笔分为一个时间段)
    _URL='http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c={c}&p={p}'
    _columns=['index','time','price','pchange','volumn','amt','bs']
    code=id2code(stockid,1)
    curl=_cURL.format(c=code)
    r=requests.get(curl)
    rx1=re.compile(r'(\d{2}:\d{2}:\d{2}~\d{2}:\d{2}:\d{2})')
    rx2=re.compile(r'[|"](\d+)/(\d{2}:\d{2}:\d{2})/(\d+\.\d{2})/(-?\d+\.\d{2})/(\d+)/(\d+)/([SMB])')
    c=len(rx1.findall(r.text))#时间段的个数等于页码数
    pages=list(range(c))#所有页码的列表
    if tail:
        i=tail%c if tail>0 else tail%-c
    else:
        i=0
    pages=pages[:-i] if i<0 else pages[-i:]
    result=[]
    for p in pages:
        url=_URL.format(c=code,p=p)
        r=requests.get(url)
        result.extend(rx2.findall(r.text))
    result=pd.DataFrame(result,columns=_columns)
    result.index=result['index']
    return result


def tt_get_FQ(stockid,start=None,end=None,limitqt=320):
    """
    获取日K线数据(后复权)
    参数：stockid:string 股票id
          start:string 开始日期:yyyy-mm-dd或yyyymmdd格式
                省略时获取从结束日期向前推limitqt条数据
          end:string 结束日期:yyyy-mm-dd或yyyymmdd格式
                省略时相当于取最后交易日
          limitqt:int 获取数据的最大数量，当选取的时间段数据量大于此限制数量时
                忽略开始日期，从结束日期向前选取限制数量的数据
    返回：
    """
    _HFQ_URL='http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param={symbol},day,{start},{end},{limitqt},hfq'
    _URL='http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param={symbol},day,{start},{end},{limitqt},'
    
    
    raise NotImplementedError('复权因子不确定，不使用此数据')


'''
数据中心(行业/地域/概念/指数)
'''

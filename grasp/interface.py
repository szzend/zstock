#coding=utf-8
'''
此模块用于对外的接口调用
'''
import pandas as pd
from requests.exceptions import ConnectTimeout
from .sina import sina_get_FQ,sina_get_datac,sina_get_catalog,sina_get_SS
from .em import em_get_profile
from .tt import tt_get_MX_x
def get_stocka(source='sina'):
    """
    获取沪深A股最后交易日的代码清单
    参数: source={em,sina,tt} 选取抓取的数据源
    返回: list(string) 股票代码
    """
    #目前仅实现了sina源
    df=sina_get_datac('hs_a')
    return list(df['code'])

def get_profile(stockid,source='em'):
    """
    获取公司基本资料
    参数: stockid 为股票代码或者代码列表或元组
          source={em,sina,tt} 选取抓取的数据源
    返回: list([code,name,company,plate,market,industry,area,capital,
            profile,business,founddate,ipodate])
    """
    #目前仅实现了em源
    result=[]
    if isinstance(stockid,list) or isinstance(stockid,tuple):
        pass
    else:
        stockid=[stockid]
    for code in stockid:
        result.append(list(em_get_profile(code)))
    return result

def get_HFQ(stockid,startdate,enddate,source='sina'):
    """
    获取时间段内后复权数据
    参数: stockid(string) 为股票代码或者代码列表或元组
          startdate(string) 开始日期,格式:yyyymmdd或yyyy-mm-dd
          enddate(string) 截止日期,格式:yyyymmdd或yyyy-mm-dd
          source={em,sina,tt} 选取抓取的数据源
    返回: DataFrame columns=[code,open,high,close,low,volume,amount,factor]
                    index=[tdate]
    """
    _columns=['code','open','high','close','low','volume','amount','factor']
    if isinstance(stockid,list) or isinstance(stockid,tuple):
        pass
    else:
        stockid=[stockid]
    #仅实现sina源
    result=[]
    drg=list(pd.date_range(startdate,enddate,freq='QS'))
    startdate=str(drg[0])
    enddate=str(drg[-1])
    drg=[(d.year,d.quarter) for d in drg]
    for code in stockid:
        tmp=[]
        for c in drg:
            tmp.append(sina_get_FQ(code,c[0],c[1]))
        df=pd.concat(tmp)
        df.insert(0,'code',code)
        df.index=pd.to_datetime(df.index)
        result.append(df)
    result=pd.concat(result)
    result.columns=_columns
    return result.sort_index().loc[startdate:enddate]

def get_MX_excel(stockid,startdate,enddate,source='tt'):
    """
    获取成交明细数据(盘后)
    参数: stockid(string) 为股票代码或者代码列表或元组
          startdate(string) 开始日期,格式:yyyymmdd或yyyy-mm-dd
          enddate(string) 截止日期,格式:yyyymmdd或yyyy-mm-dd
          source={em,sina,tt} 选取抓取的数据源
    返回: 一个DataFrame columns=[code,open,high,close,low,volume,amount,factor]
                    index=[tdate]
          及一个包含数据抓取失败的列表
    """
    #仅实现了tt源
    if isinstance(stockid,list) or isinstance(stockid,tuple):
        pass
    else:
        stockid=[stockid]
    drg=pd.date_range(startdate,enddate,freq='B')
    drg=[d.strftime('%Y%m%d ') for d in drg]
    result=[]
    failed=[]
    for code in stockid:
        lt=[]
        for tdate in drg:
            try:
                rt=tt_get_MX_x(code,tdate.strip()) #该实现可能返回None或者触发超时异常
                if not (rt is None):
                    rt.index=rt['time'].apply(lambda x:pd.to_datetime(tdate+x))
                    lt.append(rt)
            except ConnectTimeout:
                failed.append((code,tdate))
        df=pd.concat(lt)
        df.drop('time',axis=1)
        df.insert(0,'code',code)
        result.append(df)
    return pd.concat(result),failed

def get_catalog(source='sina'):
    """
    获取板块数据
    返回: DataFrame columns=['node','name','catalog','updatedate']
    """
    #仅实现了新浪分类
    _columns=['node','name','catalog','updatedate']
    result=[]
    r=sina_get_catalog()
    for k in r:
        df=pd.DataFrame()
        df['name']=r[k].index
        df.index=list(r[k]['node'])
        df['catalog']=k
        df['updatedate']=pd.Timestamp.today().strftime('%Y-%m-%d')
        result.append(df)
    return pd.concat(result)

def get_SS(stockid,source='sina'):
    """
    获取股本结构变化信息
    参数:   stockid(string)股票id
    返回:
    """
    dic={'万股':lambda x:float(x)*10000}
    def w2d(x):
        def unknown(x):
            raise ValueError('未知单位.')
        if x=='--':
            return 0
        d,w=x.split()
        dic.get(w,unknown)(d)


    _columns=['code','changedate','changelog','totalqt','ltaqt','limita','ltbqt','limitb','lthqt','updatedate']
    r=sina_get_SS(stockid)
    df=pd.DataFrame()
    df['changelog']=r['变动原因']
    df['totalqt']=r['总股本'].apply(w2d)
    df['ltaqt']=r['流通A股'].apply(w2d)
    df['limita']=r['限售A股'].apply(w2d)
    df['ltbqt']=r['流通B股'].apply(w2d)
    df['limitb']=r['限售B股'].apply(w2d)
    df['lthqt']=r['流通H股'].apply(w2d)
    df['updatedate']=pd.Timestamp.today().strftime('%Y-%m-%d')
    df.insert(0,'changedate',r.index)
    df.insert(0,'code',stockid)
    return df
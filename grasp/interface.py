#coding=utf-8
'''
此模块用于对外的接口调用
'''
import pandas as pd
from .sina import sina_get_FQ,sina_get_datac
from .em import em_get_profile
from .tt import tt_get_MX_x
def get_stocka(source='sina'):
    """
    获取沪深A股最后交易日的代码
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
    返回: DataFrame columns=[code,open,high,close,low,volume,amount,factor]
                    index=[tdate]
    """
    #仅实现了tt源
    if isinstance(stockid,list) or isinstance(stockid,tuple):
        pass
    else:
        stockid=[stockid]
    drg=pd.date_range(startdate,enddate,freq='B')
    drg=[d.strftime('%Y%m%d ') for d in drg]
    result=[]
    for code in stockid:
        lt=[]
        for tdate in drg:
            rt=tt_get_MX_x(code,tdate.strip())
            rt.index=rt['time'].apply(lambda x:pd.to_datetime(tdate+x))
            lt.append(rt)
        df=pd.concat(lt)
        df.drop('time',axis=1)
        df.insert(0,'code',code)
        result.append(df)
    return pd.concat(result)


# def _wrap_(stockid,date,market):
#     '''
#     包装查询参数，以应对不同的实现
#     参数:   stockid:string(股票代码，如000038)
#             date:string(交易日期，如20180308)
#             market:string(该股票所属市场，'sz'代表深圳,'sh'代表上海)
#     返回：一个元组:包装后的stockid及date（stockid,date)
#     '''
#     #TT实现
#     return market+stockid,date

# def get_df_MX(stockid,date,market,source=None):
#     '''
#     获取某支股票分笔明细数据 (由调用者保证股票代码及日期有效)
#     参数:   stockid:string(股票代码，如000038)
#             date:string(交易日期，格式：yyyymmdd,如20180308)
#             market:string(该股票所属市场，'sz'代表深圳,'sh'代表上海)
#     返回：  df:DataFrame(该数据包含列为:GRASP_MX_COLUMNS常量所指定的列)
#             如未获取数据则返回None
#     '''
#     symbol,date=_wrap_(stockid,date,market)
#     try:
#         d=tt_get_MX(symbol,date)
#         if d.size==0:
#             d=None
#     except:
#         return None
#     return d



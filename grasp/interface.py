#coding=utf-8
'''
此模块用于对外的接口调用
'''
from pandas import DataFrame
from ..utility import DateHelper
from .sina import sina_get_FQ,sina_get_datac
from .em import em_get_profile
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

def get_HFQ(stockid,startdate,enddate,source='sina'):
    """
    获取时间段内后复权数据
    参数: stockid(string) 为股票代码或者代码列表或元组
          startdate(string) 开始日期,格式:yyyymmdd或yyyy-mm-dd
          enddate(string) 截止日期,格式:yyyymmdd或yyyy-mm-dd
          source={em,sina,tt} 选取抓取的数据源
    """
    if isinstance(stockid,list) or isinstance(stockid,tuple):
        pass
    else:
        stockid=[stockid]
    startdate=DateHelper(startdate)
    enddate=DateHelper(enddate)
    #仅实现sina源



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


def get_df_HFQ():
    '''
    获取某支股票后复权交易数据
    参数：
    返回：
    '''
    pass

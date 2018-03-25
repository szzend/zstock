#coding=utf-8
'''
东方财富股票数据接口
相关网址:http://quote.eastmoney.com/
'''
import json
import requests
import pandas as pd
from . import headers,id2code

#股本结构及变动数据,返回json数据. 只返回最近20条记录...
#_EM_SS_URL='http://emweb.securities.eastmoney.com/PC_HSF10/CapitalStockStructure/CapitalStockStructureAjax?code=sz000068'



def em_get_profile(stockid):
    """
    获取公司基本资料
    参数:   stockid:string(股票代码，如000038)
    返回：  Series
           index=['A股代码','A股简称','公司名称','证券类别','上市交易所','所属证监会行业','注册地址','区域','注册资本(元)',
            '公司简介','经营范围','成立日期','上市日期']
    """
    #获取公司基本资料，code形如sh600666,返回json数据
    _URL='http://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax?code={symbol}'

    _index=['A股代码','A股简称','公司名称','证券类别','上市交易所','所属证监会行业','注册地址','区域','注册资本(元)',
            '公司简介','经营范围','成立日期','上市日期'
            ]

    _to={'A股代码':'agdm','A股简称':'agjc','公司名称':'gsmc','证券类别':'zqlb','上市交易所':'ssjys','所属证监会行业':'sszjhhy',
        '注册地址':'zcdz','区域':'qy','注册资本(元)':'zczb','公司简介':'gsjj','经营范围':'jyfw','成立日期':'clrq',
        '上市日期':'ssrq'
            }

    def _get_value(dict,key):
        #如果找不到相应的键值，说明字典结构已变，抛出异常
        v=dict['Result']['jbzl'].get(key) if dict['Result']['jbzl'].get(key) else dict['Result']['fxxg'].get(key)
        if not v:
            raise ValueError('数据资料已改变,未找到:"{}"'.format(key))
        return v

    url = _URL.format(symbol=id2code(stockid,1))
    import random
    r = requests.get(url, headers=random.choice(headers))
    d=json.loads(r.text)
    v=[_get_value(d,_to[key]) for key in _index]
    return pd.Series(v,index=_index)


def em_get_MX(stockid):
    """
    获取分时成交明细(最后交易日)
    参数：stockid:string,股票id,形如000038,300038,600038
    返回: DataFrame:
    """
    #返回({"result":true,"message":"ok","total":609,"value":{"pc":"4.62","data":
    #["09:24:21,4.63,1,4,0,1,0,0","10:02:27,4.62,2,2,1,1,3,1"]}})
    #id参数为股票id加上后缀(sz为2,sh为1)
    _URL = 'http://mdfm.eastmoney.com/EM_UBG_MinuteApi/Js/Get?dtype=all&rows={rows}&page={page}&id={symbol}'
    #返回的记录行数
    _rows = 1000
    #bs代表成交性质：2为买盘，1为卖盘，4为竞价？
    _rcolumns=['time','price','volume','bs','u1','u2','u3','u4']
    _columns=['成交时间','成交价格','成交量(手)','成交额(元)','性质']
    def get_json(url):
            import random
            r = requests.get(url, headers=random.choice(headers))
            try:
                d = json.loads((r.text)[1:-1])
            except json.decoder.JSONDecodeError as err:
                raise ValueError('json数据格式非预期.') from err
            c = d.get('total')  # 获取记录笔数
            if not c:
                raise ValueError('json数据格式非预期.')
            data = d.get('value', dict()).get('data')  # 获取数据
            if not data:
                raise ValueError('json数据格式非预期.')
            df = pd.DataFrame([row.split(',') for row in data])
            return c,df
        
    symbol=id2code(stockid, 2)
    url = _URL.format(rows=_rows, page=1, symbol=symbol)
    c,df=get_json(url)
    dfs=[df]
    p, _ = divmod(c, _rows)
    p = p+1 if _ else p
    t = 2
    while t <= p:
        url=_URL.format(rows=_rows,page=t,symbol=symbol)
        _,f=get_json(url)
        t+=1
        dfs.append(f)
    df=pd.concat(dfs)
    df.columns=_rcolumns
    df=df[df['bs']<'4'].astype({'price':float,'volume':int})
    df['amt']=df['price']*df['volume']
    df['bs2']=df['bs'].apply(lambda x:'买盘' if x=='2' else '卖盘') #'2'为买盘
    ix=df['time']
    df=pd.DataFrame(df,columns=['price','volume','amt','bs2'])
    df.index=ix
    df.index.name=_columns[0]
    df.columns=_columns[1:]
    return df
   

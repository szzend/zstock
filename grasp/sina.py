# coding=utf-8
"""
sina股票数据接口
"""
import requests
from lxml import etree
import pandas as pd
import re
import json
from . import headers, id2code,w2d


# 流通股份数变动数据
#_SINA_LIUTONG_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/{stockid}/stocktype/LiuTongA.phtml'


def sina_get_FQ(stockid, Y, Q):
    '''
    获取某支股票后复权交易数据(按季度每日成交数据) 
    参数:   stockid:string(股票代码，如000038)
            Y:int(交易年份，格式：yyyy)
            Q:int(季度{1,2,3,4})
    返回：  df:DataFrame
            columns: [开盘价, 最高价, 收盘价, 最低价, 交易量(股), 交易金额(元), 复权因子]
            index:['日期']

    '''
    # 后复权历史交易数据,symbol形如sz000068,Y为年份yyyy,Q为季度{1,2,3,4}
    _URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/{symbol}.phtml?year={Y}&jidu={Q}'
    url = _URL.format(symbol=id2code(stockid,1), Y=Y, Q=Q)
    import random
    r = requests.get(url, headers=random.choice(headers))
    r.encoding = 'gb2312'
    html = etree.HTML(r.text)
    tb = html.xpath('//table[@id="FundHoldSharesTable"]')
    dfs = pd.read_html(etree.tostring(
        tb[0]), header=1, skiprows=1, index_col=0, flavor='lxml')

    # 以下代码使用beautifulsoap4与html5lib作为分析器,lxml不能正确运行?
    # dfs=pd.read_html(url,attrs={'id':'FundHoldSharesTable'},header=1,index_col=0,flavor='bs4')

    return dfs[0]


def sina_get_SS(stockid):
    '''
    获取股票股本结构数据 
    参数:   stockid:string(股票代码，如000038)
    返回：  df:DataFrame
           columns: ['变动原因', '总股本', '流通A股', '高管股', '限售A股', '流通B股', '限售B股', '流通H股',
          '国家股', '国有法人股', '境内法人股', '境内发起人股', '募集法人股', '一般法人股', '战略投资者持股',
          '基金持股', '转配股', '内部职工股', '优先股']
            index:['变动日期']

    '''
    # 股本结构变动数据,网页元素.xpath('//table[contains(@id,"StockStructureNewTable")]')
    _URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/{symbol}.phtml'

    # 预期的列
    _index = ['变动原因', '总股本', '流通A股', '高管股', '限售A股', '流通B股', '限售B股', '流通H股',
              '国家股', '国有法人股', '境内法人股', '境内发起人股', '募集法人股', '一般法人股', '战略投资者持股',
              '基金持股', '转配股', '内部职工股', '优先股']

    def _check(dateframe):
        """
        检查dateframe 第一列是否与预计的_index相同
        """
        t = list(dateframe[dateframe.columns[0]])
        if len(t) != len(_index):
            return False
        t = [_index[i] in t[i] for i in range(len(_index))]
        return all(t)

    url = _URL.format(symbol=id2code(stockid, 0))
    import random
    r = requests.get(url, headers=random.choice(headers))
    r.encoding = 'gb2312'
    html = etree.HTML(r.text)
    #以下选取相应的网页元素并读取数据
    #跳过：标头(0),'公告日期(2)','股本结构图(3)',流通股(6)
    tbs = html.xpath('//table[contains(@id,"StockStructureNewTable")]')
    tbs = [etree.tostring(tb).decode('gb2312') for tb in tbs]
    tbs = ''.join(tbs)
    dfs = pd.read_html(tbs, skiprows=[0, 2, 3, 6], flavor='html5lib')
    if not _check(dfs[0]):
        raise ValueError('数据栏位非预期!')

    dfs = [df.drop(columns=df.columns[0]) for df in dfs]
    df = pd.concat(dfs, axis=1)
    df.index = _index
    df.index.name = '变动日期'
    return df.T


def sina_get_catalog():
    """
    获取新浪股票分类数据
    参数:   无
    返回:   字典,键为:'新浪行业','申万二级','热门概念','概念板块','地域板块','证监会行业','指数成分'
                值为DataFrame, index=[catalog(细分类)],columns=[node]
    """
    #返回json数据, 需去除\'才能由json正确解析
    _URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes'
    #正则表达式, 从字符串中选取相应段
    _cataloga = {'新浪行业': '\["新浪行业",\[.+"sinahy","cn"]',
                 '申万二级': '\["申万二级",\[.+"sw2_hy","cn"]',
                 '热门概念': '\["热门概念",\[.+"ch_gn","cn"]',
                 '概念板块': '\["概念板块",\[.+"gainianbankuai"]',
                 '地域板块': '\["地域板块",\[.+"diyu","cn"]',
                 '证监会行业': '\["证监会行业",\[.+"hangye","cn"]',
                 '指数成分': '\["指数成分",\[.+"zhishu","bond"]'}
    d = {}
    import random
    r = requests.get(_URL, headers=random.choice(headers))
    r.encoding = 'gb2312'
    #r=json.loads(r.text.replace('\\\'',''))
    r = r.text.replace(',""', '')
    rx = re.compile(r'\["[^\[\]]+\]')  # 取['','']形式的list
    ry = re.compile(r'[\[\]"]')
    for c in _cataloga:
        d[c] = rx.findall(re.findall(_cataloga[c], r)[0])
        d[c] = [ry.sub('', ls).split(',') for ls in d[c]]
        d[c] = pd.DataFrame(d[c])
        ix = d[c][0]
        d[c] = pd.DataFrame(d[c], columns=[1])
        d[c].index = ix
        d[c].index.name = 'catalog'
        d[c].columns = ['node']

    return d


def sina_get_datac(node, wt=None):
    """
    获取某一分类的股票数据
    参数: node:string
          wt:{0,1} 为0时返回股票代码,为1时返回代码及最后交易日交易数据
    返回: DataFrame columns=[node,code] 或
                    columns=['s代码','代码','名称','成交价','价格变动','变动比例','现买价','现卖价','昨收','开盘',
                '最高','最低','成交量','成交额','时间','unknown','市净率','总市值(万元)','流通市值(万元)','换手率']
    """
    #返回该分类下股票数量,以备分页
    _cURL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node={node}'
    #num为返回的数据数量,最大为100,asc=0 表示倒序,_s_r_a未知
    _URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={page}&num={num}&sort=symbol&asc=0&node={node}&_s_r_a=init'
    _num = 80
    _columns = ['symbol', 'code', 'name', 'trade', 'pricechange', 'changepercent', 'buy', 'sell', 'settlement', 'open', 'high','low','volume',
                'amount', 'ticktime', 'per', 'pb', 'mktcap', 'nmc', 'turnoverratio']
    _names = ['s代码','代码','名称','成交价','价格变动','变动比例','现买价','现卖价','昨收','开盘',
                '最高','最低','成交量','成交额','时间','unknown','市净率','总市值(万元)','流通市值(万元)','换手率']

    def get_codes(rawtext):
        """
        返回股票代码列表
        """
        ls = rx1.findall(rawtext)
        return [[node, code] for code in ls]

    def get_datas(rawtext):
        """
        返回所属股票最后交易日数据
        """

        # 加上"以构成正确的字典形式字符串
        ls = json.loads(rx2.sub(r'\g<1>"\g<2>"\g<3>', rawtext))
        return ls

    def wcodes(ls):
        """
        将列表转换为DataFrame
        columns=[node,code]
        """
        df = pd.DataFrame(ls, columns=['node', 'code'])
        return df

    def wdatas(ls):
        """
        """
        dtypes = {
            'symbol': str,
            'code': str,
            'name': str,
            'trade': float,
            'pricechange': float,
            'changepercent': float,
            'buy': float,
            'sell': float,
            'settlement': float,
            'open': float,
            'high': float,
            'low': float,
            'volume': int,
            'amount': int,
            'ticktime': str,
            'per': float,
            'pb': float,
            'mktcap': float,
            'nmc': float,
            'turnoverratio': float
        }
        
        mindex=pd.MultiIndex.from_tuples(list(zip(_columns,_names)))
        df = pd.DataFrame(ls,columns=_columns)
        df.astype(dtypes)
        df.columns=mindex
        return df

    curl = _cURL.format(node=node)
    r = requests.get(curl).text
    c = int(re.findall(r'String\("(\d+)"\)', r)[0])
    pgs, _ = divmod(c, _num)
    pgs = pgs+1 if _ else pgs
    rx1 = re.compile(r'code:"(\d{6})"')  # 提取股票代码
    rx2 = re.compile(r'([{,])([a-z]+?)(:)')  # 加上"以构成正确的字典形式字符串
    import random
    rt = []
    f = get_datas if wt else get_codes
    w = wdatas if wt else wcodes
    for i in range(1, pgs+1):
        url = _URL.format(page=i, node=node, num=_num)
        r = requests.get(url, headers=random.choice(headers))
        r.encoding = 'gb2312'
        r = r.text
        rt.extend(f(r))
    return w(rt)


def sina_get_GN(stockid):
    """
    获取股票所属概念板块
    参数:stockid:string 股票代码
    返回: DataFrame columns=['code','name']
    """
    #symbol形如sz00002266
    _URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getSymbolGN?symbol={symbol}'
    url = _URL.format(symbol=id2code(stockid, 1))
    r = requests.get(url)
    r.encoding = 'gb2312'
    rx = re.compile(r'{type:"(\w+?)",name:"(\w+?)"}')
    df = pd.DataFrame(rx.findall(r.text), columns=['code', 'name'])
    return df


def sina_get_trade(stockid):
    """
    获取实时交易数据
    参数:stockid:string或list(str) 股票代码或代码列表
    返回:DataFrame columns=['代码','名称','开盘','昨收','最新','最高','最低','买一','卖一','成交量(股)','成交额(元)','买一量(股)','买一价',
        '买二量(股)','买二价','买三量(股)','买三价','买四量(股)','买四价','买五量(股)','买五价','卖一量(股)','卖一价','卖二量(股)','卖二价',
        '卖三量(股)','卖三价','卖四量(股)','卖四价','卖五量(股)','卖五价','日期','时间','null']
        index=[code]
    """
    #ls形如sz002266,sh600555
    _URL = 'http://hq.sinajs.cn/?list={ls}'
    #获取到的数据结构
    _columns = ['code', 'name', 'open', 'lclose', 'trade', 'high', 'low', 'b1', 's1', 'volume', 'amt', 'b1_q', 'b1_p',
                'b2_q', 'b2_p', 'b3_q', 'b3_p', 'b4_q', 'b4_p', 'b5_q', 'b5_p', 's1_q', 's1_p', 's2_q', 's2_p', 's3_q',
                's3_p', 's4_q', 's4_p', 's5_q', 's5_p', 'date', 'time', 'null']

    _names = ['代码', '名称', '开盘', '昨收', '最新', '最高', '最低', '买一', '卖一', '成交量(股)', '成交额(元)', '买一量(股)', '买一价',
              '买二量(股)', '买二价', '买三量(股)', '买三价', '买四量(股)', '买四价', '买五量(股)', '买五价', '卖一量(股)', '卖一价', '卖二量(股)', '卖二价',
              '卖三量(股)', '卖三价', '卖四量(股)', '卖四价', '卖五量(股)', '卖五价', '日期', '时间', 'null']

    s = None
    if isinstance(stockid, list):
        s = [id2code(s, 1) for s in stockid]
        s = ','.join(s)
    ls = id2code(stockid, 1) if not s else s
    url = _URL.format(ls=ls)
    r = requests.get(url)
    r.encoding = 'gb2312'
    r = r.text
    rx1 = re.compile(r'[sh|sz](\d{6})=')
    rx2 = re.compile(r'="(\S+?)";')
    code = rx1.findall(r)
    data = [s.split(',') for s in rx2.findall(r)]
    mindex = pd.MultiIndex.from_tuples(list(zip(_columns[1:], _names[1:])))
    df = pd.DataFrame(data, index=code, columns=mindex)
    df.index.name = _names[0]
    return df

def _sina_get_info(stockid):
    """
    获取
    """
    _URL='http://finance.sina.com.cn/realstock/company/{symbol}/jsvar.js'
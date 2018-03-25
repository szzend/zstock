#coding=utf-8
ifeng.com

'''
凤凰网K线数据，含分钟、日、周、月。无自选时间段参数。

K_TYPE = {'D': 'akdaily', 'W': 'akweekly', 'M': 'akmonthly'}
http://api.finance.ifeng.com/akdaily/?code=sh600848&type=last
http://api.finance.ifeng.com/akweekly/?code=sh600848&type=last
http://api.finance.ifeng.com/akmonthly/?code=sh600848&type=last

K_MIN_LABELS = ['5', '15', '30', '60']
http://api.finance.ifeng.com/akmin?scode=sh600848&type=5

'''

'''
以xls格式获取某日分笔数据
#新浪分笔数量稍有差异
#腾讯笔数正确，金额稍有差异
#网易相差较大
TICK_PRICE_URL = 'http://market.finance.sina.com.cn/downxls.php?date=2018-03-08&symbol=sh600848'
TICK_PRICE_URL_TT = 'http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=sh600848&d=20180308'
TICK_PRICE_URL_NT = 'http://quotes.money.163.com/cjmx/2018/20180308/0600848.xls'


'''
'''
#新浪网页分笔数据，数据精度同xls下载
TODAY_TICKS_PAGE_URL = '%s%s/quotes_service/api/%s/CN_Transactions.getAllPageTime?date=%s&symbol=%s'
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date=2018-03-08&symbol=sh600848

TODAY_TICKS_URL = '%s%s/quotes_service/view/%s?symbol=%s&date=%s&page=%s'
http://vip.stock.finance.sina.com.cn//quotes_service/view/vMS_tradedetail.php?symbol=sh600848&date=2018-03-08&page=1

'''

'''
获取实时交易数据
LIVE_DATA_URL = 'http://hq.sinajs.cn/rn=%s&list=%s'
#list=sh600848,sz000008  rn可选?


'''
'''
#获取历史交易数据（日复权数据）
HIST_FQ_URL =    'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/sh600848.phtml?year=2018&jidu=1'
                  http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/000725.phtml
#历史交易日数据
                  http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000725.phtml?year=2001&jidu=1
HIST_INDEX_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/sh000001/type/S.phtml?year=2018&jidu=1'  ??
HIST_FQ_FACTOR_URL = 'http://vip.stock.finance.sina.com.cn/api/json.php/BasicStockSrv.getStockFuQuanData?symbol=sh600848&type=hfq'
'''
#获取指数行情数据
INDEX_HQ_URL = '''http://hq.sinajs.cn/rn=xppzh&list=sh000001,sh000002,sh000003,sh000008,sh000009,sh000010,sh000011,sh000012,sh000016,sh000017,sh000300,sh000905,sz399001,sz399002,sz399003,sz399004,sz399005,sz399006,sz399008,sz399100,sz399101,sz399106,sz399107,sz399108,sz399333,sz399606'''

#腾讯获取K线数据
KLINE_TT_URL = 'http://web.ifzq.gtimg.cn/appstock/app/%skline/get?_var=kline_day%s&param=%s,%s,%s,%s,640,%s&r=0.%s'

http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh600848,day,,,320,qfq&r=0.8055485478026063
http://web.ifzq.gtimg.cn/appstock/app/kline/kline?_var=kline_day&param=sh600848,day,,,320,&r=0.6273812904223054
http://ifzq.gtimg.cn/appstock/app/kline/mkline?param=sh600848,m5,,320&_var=m5_today&r=0.8031780945636215
http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_weekqfq&param=sh600848,week,,,320,qfq&r=0.07522339051645777


#处理当日行情分页数据，格式为json
DAY_PRICE_MIN_URL = '%sapi.finance.%s/akmin?scode=%s&type=%s'
SINA_DAY_PRICE_URL = '%s%s/quotes_service/api/%s/Market_Center.getHQNodeData?num=80&sort=code&asc=0&node=%s&symbol=&_s_r_a=page&page=%s'
# SINA_DAY_PRICE_URL = '%s%s/quotes_service/api/%s/Market_Center.getHQNodeData?num=10000&node=%s'

http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=15&sort=changepercent&asc=0&node=sh_a&symbol=
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getSymbolGN?symbol=sh600635
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?node=hs_a&page=1
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=hangye_ZA01
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=hangye_ZA01&symbol=&_s_r_a=init
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=hangye_ZA01&symbol=&_s_r_a=auto
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=hangye_ZA01&symbol=&_s_r_a=auto
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getSymbolGN?symbol=sh600506
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=hangye_ZA09
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=hangye_ZA09&symbol=&_s_r_a=init
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getSymbolGN?symbol=sh600635
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getSymbolGN?symbol=sh600895
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=15&sort=changepercent&asc=0&node=sh_a&symbol=

http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getRTHKStockCount?node=qbgg_hk
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getRTHKStockData?page=1&num=5&sort=changepercent&asc=0&node=qbgg_hk

http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFundNetCount?page=1&num=5&sort=date&asc=0&node=open_fund
http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getFundNetData?page=1&num=5&sort=date&asc=0&node=open_fund


http://hq.sinajs.cn/rn=1521252145482&list=s_sh000001,s_sz399001,s_sz399415,s_sz395099
http://hq.sinajs.cn/rn=dd4ty&list=sh600635,sh600895,sh600213,sh603778,sh600865

http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes

http://finance.sina.com.cn/realstock/company/sz300688/jsvar.js

http://data.eastmoney.com/gstc/search.ashx?PageIndex=1&PageSize=100

http://stock.gtimg.cn/data/index.php?appn=detail&action=timeline&c=sz300164
http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c=sz300164&p=12
http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param=sh600505,day,,,320,hfq&r=0.8479123318393149
http://web.ifzq.gtimg.cn/appstock/app/kline/kline?_var=kline_daynull&param=sh600505,day,,,320,&r=0.48183172674232333
http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param=sh600505,day,,,320,hfq&r=0.7138570473696857
http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh600505,day,2012-01-01,2012-12-31,320,qfq&r=0.5393342403979358

#coding: utf-8
"""
此模块实现爬取，调度及辅助工具
"""
import asyncio 
from aiohttp import ClientSession

http_agent=[
    {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:58.0) Gecko/20100101 Firefox/58.0'
    },
    {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        #'Referer': 'http://vip.stock.finance.sina.com.cn/mkt/',
        'Content-type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive'
    },
    {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
    }
]

class Crawler:
    """
    """
    def __init__(self,spider):
        pass
        
    def run(self):
        pass

#coding: utf-8

from multiprocessing import Queue
from logging.handlers import QueueListener,QueueHandler,TimedRotatingFileHandler
import logging
import sys
from collections import defaultdict
from .settings import Settings
import time


class Logger:
    """
    用于记录抓取过程
    """

    class CounterHandler(logging.NullHandler):
        def __init__(self,save_result=True):
            super().__init__()
            self.__counter=defaultdict(int)
            self.__result=defaultdict(list)
            self.__save_result=save_result

        def handle(self,record):
            self.__counter[record.levelname]+=1
            if self.__save_result:
                self.__result[record.levelname].append(record.message)

        def report(self):
            t=[self.__counter[i] for i in self.__counter]
            t=sum(t)
            s=[f'记录{i}有:{self.__counter[i]} 个' for i in self.__counter]
            s='\n'.join(s)
            s=f'共有:{t} 个记录,其中\n'+s
            return s

        def result(self):
            if self.__save_result:
                return self.__result

    def __init__(self,debug=False):
        """
        当debug为True时，不记录到日志文件，只输出到控制台
        """
        self.debug=debug
        self.__q=Queue()
        self.__counter=None
        self.__file_handler=TimedRotatingFileHandler('crawler.log',when='D',interval=3,encoding='utf-8')
        self.__stdout=logging.StreamHandler(sys.stdout)
        self.__qh=QueueHandler(self.__q)
        self.__logger=logging.getLogger('logger.Logger')
        self.__logger.setLevel(20)
        self.__listener=None
        self.__time=None
        



    def start(self,save_result=True):
        self.__logger.addHandler(self.__qh)
        self.__counter=self.CounterHandler(save_result)
        if self.debug:
            self.__logger.addHandler(self.__stdout)
            self.__listener=QueueListener(self.__q,self.__counter)
        else:
            self.__listener=QueueListener(self.__q,self.__counter,self.__file_handler)
        self.__listener.start()
        self.__time=time.time()
    def stop(self):
        self.__time=time.time()-self.__time
        self.__listener.stop()
        self.__logger.handlers=[]
        self.__listener.handlers=[]

    def info(self,msg, *args, **kwargs):
        self.__logger.info(msg,*args, **kwargs)

    def warning(self,msg,*args, **kwargs):
        self.__logger.warning(msg,*args, **kwargs)

    def error(self,msg,*args, **kwargs):
        self.__logger.error(msg,*args, **kwargs)

    def report(self):
        return f'运行时间：{self.__time}.\n{self.__counter.report()}'
        
    def result(self):
        return self.__counter.result()

     
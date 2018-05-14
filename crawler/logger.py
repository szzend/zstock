#coding: utf-8

from multiprocessing import Queue
from logging.handlers import QueueListener,QueueHandler,TimedRotatingFileHandler
import logging
from collections import defaultdict




lg=logging.getLogger(__name__)
q=Queue()
qh=QueueHandler(q)
lg.addHandler(qh)
#fh=TimedRotatingFileHandler('log.txt')
h1=listener()
ler=QueueListener(q,h1)




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
            return self.__result

    def __init__(self,debug=False):
        """
        当debug为True时，不记录到日志文件，只输出到控制台
        """
        self.debug=debug
        self.__q=Queue()

    def start(self):
        pass

    def stop(self):
        pass

    def info(self):
        raise NotImplementedError

    def warning(self):
        pass

    def error(self):
        pass

    def report(self):
        pass

     
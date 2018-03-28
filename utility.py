import re
import time
import datetime
class DateHelper():
    """
    """
    def __init__(self,strdate):
        rx=re.compile(r'(?P<y>\d{4})([-/]?)(?P<m>\d{2})\2(?P<d>\d{2})')
        rlt=rx.match(strdate)
        if not rlt:
            raise ValueError('{}不是有效日期格式'.format(strdate))
        self.__date=datetime.date(int(rlt.group('y')),int(rlt.group('m')),int(rlt.group('d')))
    @property
    def quarter(self):
       j=[0,1,1,1,2,2,2,3,3,3,4,4,4]
       return j[self.__date.month]
    @property
    def year(self):
        return self.__date.year
    @property
    def month(self):
        return self.__date.month
    @property
    def day(self):
        return self.__date.day
    @property
    def tuple(self):
        return self.__date.year,self.__date.month,self.__date.day

    def __str__(self):
        return datetime.date.strftime(self.__date,'%Y-%m-%d')
        
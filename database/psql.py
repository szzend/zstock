#coding=utf-8
"""
postgresql数据库系统实现

"""
import psycopg2

def get_conn():
    """
    根据服务器实际配置获取预设的数据库连接
    """
    return psycopg2.connect('dbname=zstock user=zsk')


def initdb(conn):
    """
    构建相应的数据表
    参数:
    返回：
    """
    #创建表模式
    sq1='''create schema zsk;'''
    #基本资料表
    sq2='''
        create table stocka(
            code text primary key,
            name text,
            company text,
            plate text,
            market text,
            industry text,
            area text,
            capital text,
            profile text,
            business text,
            founddate date,
            ipodate date
        );'''
    #日复权数据分区表
    sq3='''
        create table daydatafq(
            code text not null,
            tdate date not null,
            open float not null,
            high float not null,
            close float not null,
            low float not null,
            volume bigint not null,
            amount bigint not null,
            factor float not null,
            turnoverratio float
        ) partition by range(tdate);
        '''
    #创建日复权数据各分区。索引待创建。。。
    sq31='''
        create table y2008_y2011 partition of daydatafq
        for values from ('2008-01-01') to ('2011-12-31');

        create table y2012_y2014 partition of daydatafq
        for values from ('2012-01-01') to ('2014-12-31');

        create table y2015_y2017 partition of daydatafq
        for values from ('2015-01-01') to ('2017-12-31');

        create table y2018_y2020 partition of daydatafq
        for values from ('2018-01-01') to ('2020-12-31');

        '''
    
    #股本结构表
    sq3='''
        create table SS(
            code text primary key,
            changedate date,
            changelog text,
            totalqt bigint,
            ltaqt bigint,
            limita bigint,
            ltbqt bigint,
            limitb bigint,
            lthqt bigint,
            updatedate date
        );
    '''

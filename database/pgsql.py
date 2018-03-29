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
            ipodate date,
            updatedate date);
    '''
    #日复权数据分区表
    sq3='''
        create table daydatafq(
            tdate date not null,
            code text not null,
            open float not null,
            high float not null,
            close float not null,
            low float not null,
            volume bigint not null,
            amount bigint not null,
            factor float not null,
            turnoverratio float)
        partition by range(tdate);
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
    sq4='''
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
    #板块分类资料表
    sq5='''
    create table catalog(
            node text primary key,
            name text,
            catalog text,
            updatedate date
        );
    '''
    #股票分板块表
    sq6='''
    create table code2catalog(
            node text references catalog (node),
            code text references stocka (code),
            updatedate date,
            primary key (node,code)
        );
    '''
    #成交明细表
    sq7='''
    create table sz_detail(
            code text,
            tdate date,
            time time,
            price float,
            volume int,
            amount int,
            bs text)
        partition by range(tdate);
    '''
    sq71='''
    create table sz_ym201803 partition of sz_detail
    for values from ('2018-03-01') to ('2018-03-31');

    create table sz_ym201804 partition of sz_detail
    for values from ('2018-04-01') to ('2018-04-30');
    '''
    sq8='''
    create table sh_detail(
            code text,
            tdate date,
            time time,
            price float,
            volume int,
            amount int,
            bs text)
        partition by range(tdate);
    '''
    sq81='''
    create table sh_ym201803 partition of sh_detail
    for values from ('2018-03-01') to ('2018-03-31');

    create table sh_ym201804 partition of sh_detail
    for values from ('2018-04-01') to ('2018-04-30');
    '''
    sql=''.join([sq1,sq2,sq3,sq31,sq4,sq5,sq6,sq7,sq71,sq8,sq81])
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)


def insert_stocka():
    
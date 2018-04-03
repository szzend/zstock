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
    sql=''.join([sq1,sq2,sq3,sq31,sq4,sq5,sq6,sq7,sq71,sq8,sq81])
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)


def insert_stocka():
    
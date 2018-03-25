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


def initdb():
    """
    构建相应的数据表
    """

    

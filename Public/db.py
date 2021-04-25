# -*- coding: utf-8 -*-
from typing import TypeVar

import pymysql
from Public.logs import logger
from Config.setting import MYSQL

T = TypeVar('T')  # 可以是任何类型


class Mysql:
    """
    mysql 操作类  demo  Mysql.select('SELECT * FROM `case`')
    """

    @classmethod
    def mysql(cls):
        """
        Mysql 连接
        :return:  str  Mysql连接串
        """
        try:
            conn = pymysql.connect(**MYSQL)
            return conn
        except Exception as e:
            logger.error(f'Mysql客户端连接失败! {e}')

    @classmethod
    def select(cls, sql):
        """
        SQL 操作   "select * from  `case`"
        :param sql:  str sql
        :return:  type
        """
        try:
            conn = cls.mysql()
            cur = conn.cursor()
            cur.execute(sql)
            select_data = cur.fetchall()
            cur.close()
            conn.close()
            return select_data
        except Exception as e:
            logger.error(f'执行Mysql sql错误{e}')



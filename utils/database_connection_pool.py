import pymysql
from DBUtils.PooledDB import PooledDB


class OPMysql(object):
    __pool = None

    def __init__(self, mysqlInfo):
        # 构造函数，创建数据库连接、游标
        self.coon = OPMysql.getmysqlconn(mysqlInfo)
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)
        # self.cur = self.coon.cursor()

    # 数据库连接池连接
    @staticmethod
    def getmysqlconn(mysqlInfo):
        if OPMysql.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=mysqlInfo['host'],
                              user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], db=mysqlInfo['db'],
                              port=mysqlInfo['port'])
            print(__pool)
        return __pool.connection()

    # 插入\更新\删除sql
    def op_insert_update_del(self, sql):
        print('op_insert', sql)
        insert_num = self.cur.execute(sql)
        print('mysql sucess ', insert_num)
        self.coon.commit()
        return insert_num

    # 查询
    def op_select(self, sql, shownum=False):
        print('op_select', sql)
        ret = self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchall()  # 返回结果为字典
        print('op_select', select_res)
        if shownum:
            return ret, select_res
        return select_res

    # 释放资源
    def dispose(self):
        # 并不是真正意义的关闭 pymysql是关闭与数据库的连接 这个是把从连接池中拿到的连接放回去
        self.coon.close()
        self.cur.close()


if __name__ == '__main__':
    from config import local_setting

    mysqlInfo = {
        'host': local_setting.SHOST,
        'port': local_setting.SPORT,
        'user': local_setting.SUSER,
        'passwd': local_setting.SPASSWD,
        'db': local_setting.SDATABASE
    }
    # 申请资源
    opm = OPMysql(mysqlInfo)

    sql = "select * from need2crawl limit 100"
    res = opm.op_select(sql, True)
    # 释放资源
    opm.dispose()

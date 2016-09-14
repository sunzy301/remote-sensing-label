# coding=utf-8
# the class of ground truth
import sqlite3

class GroundTruth(object):
    def __init__(self):
        self._GTClass = {0: "vegetation",
                        1: "buildings",
                        2: "road",
                        3: "water",
                        4: "bare soil",
                        5: "wetland",
                        6: "farmland",
                        7: "shadow"
                        }
        self._num = len(self._GTClass)

    @property
    def GTClass(self):
        return self._GTClass

    @property
    def num(self):
        return self._num

    def insert_into_table(self, conn, name):
        """
        将ground truth信息插入label_name表格中
        :param conn: 数据库链接
        :param name:遥感图像名称
        :return:
        """
        for k, v in self._GTClass.items():
            insert_sql = '''INSERT INTO %s_label_name VALUES (%d, '%s')''' % (name, k, v)
            print(insert_sql)
            conn.execute(insert_sql)
        conn.commit()
# coding=utf-8
# 用于删除sqlite中某个table的全部数据
# 仅用于测试
import sqlite3

from CaffeProject.util.parameter import Para
with sqlite3.connect(Para.db_name) as conn:
    rs_name = "GF2_shanghai"
    conn.execute("delete from %s_label" % rs_name)
    conn.commit()

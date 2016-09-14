# coding = utf-8
import sqlite3

from CaffeProject.util.parameter import Para
with sqlite3.connect(Para.db_name) as conn:

    # n = 1
    # for i in range(10):
    #     for j in range(5):
    #         conn.execute("INSERT INTO GF2_Shanghai_label VALUES(%d, 1, 6, 120.2, 31.2, %d);" % (n, i))
    #         n += 1
    # conn.commit()
    cursor = conn.execute("select ID, LABEL from GF2_Shanghai_label")
    for row in cursor:
        print(row)

# mysql demo
import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='Sunzy12315', db='world', port=3306)

    # cursor游标
    # 默认游标返回元组
    cur = conn.cursor()
    cur.execute("select * from city")

    # fetchall取回所有行
    # 返回的结果是元组
    # lines = cur.fetchall()
    # for line in lines:
    #     print(line)

    # rowcount行的数量
    # fetchone每次取回一行
    num = int(cur.rowcount)
    print(num)
    for i in range(num):
        line = cur.fetchone()
        print(line[0])

    # 可以设置不同的游标，使得返回的是dict
    # dict的key就是列名,列名区分大小写
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("select * from city")
    lines = cur.fetchall()
    for line in lines:
        print(line["Name"])

    # 输出列名
    desc = cur.description
    for i in range(len(desc)):
        print(desc[i][0])

    # 格式化选择
    # 使用类似于C的格式化方法
    cur.execute("select * from city where ID=%s", ("1"))
    line = cur.fetchone()
    print(line)

except BaseException as e:
    print(e.with_traceback())
finally:
    if conn:
        conn.close()
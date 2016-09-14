# coding=utf-8
# sqlite测试
# python内置sqlite，使用简单
import sqlite3

def main():
    with sqlite3.connect("e:\\temp\\rs\\db\\first.db") as conn:
        print("connect success")
        # conn.execute('''CREATE TABLE COMPANY
        # (ID INT PRIMARY KEY     NOT NULL,
        # NAME           TEXT    NOT NULL,
        # AGE            INT     NOT NULL,
        # ADDRESS        CHAR(50),
        # SALARY         REAL);''')
        #
        # conn.commit()
        print("create table")

        # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        # VALUES (1, 'Paul', 32, 'California', 20000.00 )")
        #
        # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        # VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
        #
        # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        # VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
        #
        # conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        # VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
        #
        # conn.commit()
        print("Records created successfully")

        cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("ADDRESS = ", row[2])
            print("SALARY = ", row[3], "\n")

        print("Operation done successfully")


if __name__ == "__main__":
    main()
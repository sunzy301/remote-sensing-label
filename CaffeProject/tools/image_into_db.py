# coding=utf-8
# 主要是将pano数据放入sqlite数据库
import os
import re

# import MySQLdb
import sqlite3

from CaffeProject.util.parameter import Para

# def put_into_mysql(dir_name):
#     """
#     旧版插入数据库函数，使用mysql
#     不再使用
#     :param dir_name:
#     :return:
#     """
#     try:
#         conn = MySQLdb.connect(host='localhost', user='root', passwd='Sunzy12315', db='demo', port=3306, charset="utf8")
#         cur = conn.cursor()
#         url = ""
#         values = []
#         for file_name in os.listdir(dir_name):
#             print(file_name)
#             type_file = file_name.split(".")[-1]
#             if type_file == "jpg":
#                 url = os.path.join(dir_name, file_name)
#             else:
#                 # load .txt file
#                 with open(os.path.join(dir_name, file_name)) as f:
#                     gis_info = f.readline()
#                     print(gis_info)
#                     lat, lng = generate_lat_lng(gis_info)
#                     location = f.readline()[:-1]#.decencode(encoding="utf-8")
#                     title = f.readline()[:-1]#.encode(encoding="utf-8")
#                     tag = f.readline()[:-1]#.encode(encoding="utf-8")
#                     user = f.readline()
#                     camera = f.readline()#.encode(encoding="utf-8")
#                     temp = (int(file_name.split(".")[0]), lat, lng, url, location, title, tag, camera)
#                     print(temp)
#                     values.append(temp)
#         cur.executemany("insert into pano_images values (%s, %s, %s, %s, %s, %s, %s, %s)", values)
#         conn.commit()
#
#     except BaseException as e:
#         print(e.with_traceback())

def put_into_db(dir_name):
    """
    将pano的图片文件插入sqlite数据库
    :param dir_name:pano图像文件所在文件夹
    :return:
    """
    values = []
    with sqlite3.connect(Para.db_name) as conn:
        cur = conn.cursor()
        for file_name in os.listdir(dir_name):
            print(file_name)
            type_file = file_name.split(".")[-1]
            if type_file == "jpg":
                url = os.path.join(dir_name, file_name)
            else:
                # load .txt file
                with open(os.path.join(dir_name, file_name)) as f:
                    gis_info = f.readline()
                    print(gis_info)
                    lat, lng = generate_lat_lng(gis_info)
                    location = f.readline()[:-1]#.decencode(encoding="utf-8")
                    title = f.readline()[:-1]#.encode(encoding="utf-8")
                    tag = f.readline()[:-1]#.encode(encoding="utf-8")
                    user = f.readline()
                    camera = f.readline()#.encode(encoding="utf-8")
                    temp = (int(file_name.split(".")[0]), lat, lng, url, location, title, tag, camera)
                    print(temp)
                    values.append(temp)
        cur.executemany("insert into pano_images values (?,?,?,?,?,?,?,?)", values)
        conn.commit()

def generate_lat_lng(gis_info):
    splits = re.split("N\?|E", gis_info)
    # lat
    lat_splits = re.split("°|'|\"| ", splits[0])
    lat = int(lat_splits[0]) + int(lat_splits[2])/60.0 + float(lat_splits[4])/3600.0
    # lng
    lng_splits = re.split("°|'|\"| ", splits[1])
    # print(float(lng_splits[3]))
    lng = int(lng_splits[1]) + int(lng_splits[3])/60.0 + float(lng_splits[5])/3600.0
    return lat, lng

def create_pano_db():
    with sqlite3.connect(Para.db_name) as conn:
        create_sql = '''CREATE TABLE `pano_images` (
        `ID` INT UNSIGNED NOT NULL ,
        `LAT` DOUBLE NOT NULL,
        `LNG` DOUBLE NOT NULL,
        `URL` VARCHAR(45) NOT NULL ,
        `LOCATION` VARCHAR(45) NULL ,
        `TITLE` VARCHAR(45) NULL ,
        `TAG` VARCHAR(45) NULL ,
        `CAMERA` VARCHAR(45) NULL ,
        PRIMARY KEY (`ID`));'''
        create_index_id = '''CREATE INDEX pano_images_id
        ON pano_images (ID);'''
        create_index_lat = '''CREATE INDEX pano_images_lat
        ON pano_images (LAT);'''
        create_index_lng = '''CREATE INDEX pano_images_lng
        ON pano_images (LNG);'''

        # print(create_sql)
        conn.execute(create_sql)
        conn.execute(create_index_id)
        conn.execute(create_index_lat)
        conn.execute(create_index_lng)
        conn.commit()

def test_select_from_db():
    """
    测试图像信息数据是否存入数据库
    :return:
    """
    with sqlite3.connect(Para.db_name) as conn:
        cursor = conn.execute("select * from pano_images")
        for row in cursor:
            print(row)

def main():
    # create pano db in sqlite3
    # create_pano_db()

    # insert into db
    # put_into_db("E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\pano\\lujiazui")

    # test
    test_select_from_db()

if __name__ == "__main__":
    #put_into_mysql("E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\pano\\lujiazui")
    main()
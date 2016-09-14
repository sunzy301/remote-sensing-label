# coding=utf-8
# 在数据库中检索pano数据集
# 两个实验：
# 1 检索所有图片
# 2 检索某个坐标点附近图片

import MySQLdb

from CaffeProject.util import basic_func

def retrieval_all_images():
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='Sunzy12315', db='demo', port=3306, charset="utf8")
        cur = conn.cursor()
        retrieval_sql = "select ID, URL from pano_images"
        cur.execute(retrieval_sql)
        row_num = int(cur.rowcount)
        for i in range(row_num):
            line = cur.fetchone()
            print(line[1])
    except BaseException as e:
        print(e.with_traceback())

def retrieval_images_around_location(x, y):
    # 经纬度阈值
    e = 0.001
    # 距离阈值，单位是千米
    ed = 0.1
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='Sunzy12315', db='demo', port=3306, charset="utf8")
        cur = conn.cursor()
        # 使用在数据库中粗糙的判断，是一个围绕标记位置的矩形，实际应该为圆形
        sql = "SELECT ID, LAT, LNG, URL FROM pano_images WHERE ABS(LAT-%s)<%s and ABS(LNG-%s)<%s" % (x, e, y, e)
        print(sql)
        cur.execute(sql)
        num = int(cur.rowcount)
        print(num)
        index = 0
        for i in range(num):
            line = cur.fetchone()
            lat = line[1]
            lon = line[2]
            url = line[3]
            # print(lat, lon, url)
            # 判断距离是否小于阈值，小于才会添加进数据集
            if basic_func.distanceEarth(x, y, lat, lon) < ed:
                print(i, url)
    except BaseException as e:
        print(e.with_traceback())

if __name__ == "__main__":
    # retrieval_all_images()
    # retrieval_all_images() test done
    retrieval_images_around_location(31.239, 121.495)
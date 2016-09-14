# coding=utf-8
# 照片数据集类

import os
# import MySQLdb

import sqlite3

from CaffeProject.util.socialmedia_image import *
from CaffeProject.util import basic_func
from CaffeProject.util import parameter

class ImageSet(object):
    """
    主要部分就是一个dict
    key是id，value是SMImage对象
    """
    # 特征的维度
    featureNum = 4096

    def __init__(self, name):
        self.__name = name
        self.__iset = {}

    @property
    def image_set(self):
        return self.__iset

    def add(self, key, value):
        """
        往map中添加项，进行参数检查
        :param key: id
        :param value: SMImage对象
        :return:
        """
        if key in self.__iset:
            return -1
        else:
            self.__iset[key] = value
            return 0

    def load_all(self):
        """
        读取所有没有读过的图片，格式是numpy的array矩阵
        :return:
        """
        for (k, v) in self.__iset.items():
            if v.imageArray is None:
                v.get_image_array()

    def get_images_from_dir(self, dirname):
        """
        从一个文件夹中读取图片，所有图片编号为数字
        :param dirname: 文件夹地址
        :return:
        """
        image_files = [x for x in os.listdir(dirname)]
        for filename in image_files:
            if os.path.splitext(filename)[1] != ".jpg":
                continue
            index = os.path.splitext(filename)[0]
            # 所有图片的编号从0开始
            image = SMImage(int(index)-1, os.path.join(dirname, filename))
            self.add(int(index)-1, image)
        self.load_all()

    def get_images_from_dir_2(self, dirname):
        """
        从一个文件夹中读取图片，图片文件名没有限制
        :param dirname: 文件夹地址
        :return:
        """
        image_files = [x for x in os.listdir(dirname)]
        num = 0
        for filename in image_files:
            if os.path.splitext(filename)[1] != ".jpg":
                continue
            # index = os.path.splitext(filename)[0]
            # 所有图片的编号从0开始
            image = SMImage(num-1, os.path.join(dirname, filename))
            self.add(num-1, image)
            num += 1
        self.load_all()



    def get_social_media_images_from_db(self, lat, lng):
        """
        在社交媒体照片数据库中检索某个位置附近的照片
        :param lat:
        :param lng:
        :return:
        """
        # 经纬度阈值
        e = 0.001
        # 距离阈值，单位是千米
        ed = 0.2
        with sqlite3.connect(parameter.Para.db_name) as conn:
            # 使用在数据库中粗糙的判断，是一个围绕标记位置的矩形，实际应该为圆形
            sql = "SELECT LAT, LNG, URL FROM pano_images WHERE ABS(LAT-%f)<%f and ABS(LNG-%f)<%f" % (lat, e, lng, e)
            print(sql)
            cur = conn.execute(sql)
            index = 0
            for line in cur:
                lat = line[0]
                lon = line[1]
                url = line[2]
                print(lat, lon, url)
                # 判断距离是否小于阈值，小于才会添加进数据集
                if basic_func.distanceEarth(lat, lng, lat, lon) < ed:
                    image = SMImage(index, url)
                    self.add(index, image)
                    index += 1

    # def get_social_media_images(self, x, y):
    #     """
    #     老版本函数，从mysql中获取，不再使用
    #     根据遥感样本的位置，从数据库中读取对应的图像数据，包括图像数据的信息和文件位置
    #     从数据库中根据矩形范围粗略检索图片，然后精细计算图片与位置距离
    #     :param x:
    #     :param y:
    #     :return:
    #     """
    #     # 经纬度阈值
    #     e = 0.001
    #     # 距离阈值，单位是千米
    #     ed = 0.2
    #     try:
    #         conn = MySQLdb.connect(host='localhost', user='root', passwd='Sunzy12315', db='world', port=3306)
    #         cur = conn.cursor()
    #         # 使用在数据库中粗糙的判断，是一个围绕标记位置的矩形，实际应该为圆形
    #         sql = "SELECT LAT, LON, URL FROM IMAGES WHERE ABS(LAT-"+x+")<"+e+" and ABS(LON-"+y+")<"+e
    #         cur.execute(sql)
    #         num = int(cur.rowcount)
    #         print(num)
    #         index = 0
    #         for i in range(num):
    #             line = cur.fetchone()
    #             lat = line[0]
    #             lon = line[1]
    #             url = line[2]
    #             # 判断距离是否小于阈值，小于才会添加进数据集
    #             if basic_func.distanceEarth(x, y, lat, lon) < ed:
    #                 image = SMImage(index, url)
    #                 self.add(index, url)
    #
    #
    #     except BaseException as e:
    #         print(e.with_traceback())
    #     finally:
    #         if conn:
    #             # conn.close()

if __name__ == "__main__":
    # IS = ImageSet()
    # image = SMImage(0, "e:\\test.jpg")
    # IS.add(0, image)
    # IS.load_all()
    # print(IS.iset[0].filename)
    # print(IS.iset[0].imageArray.shape)

    # dirname = "E:\\sun2\\工作\\python\\CaffeProject\\CaffeProject\\Crawler\\data\\hello"
    # IS = ImageSet()
    # IS.get_images_from_dir(dirname)
    # print(IS.image_set[1].imageArray.shape)
    IS = ImageSet("GF2_shanghai")
    IS.get_social_media_images_from_db(31.242, 121.497)
    IS.load_all()
    for k, v in IS.image_set.items():
        print(k, " ", v.filename)
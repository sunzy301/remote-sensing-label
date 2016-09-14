# coding=utf-8
# 遥感图像像素
import numpy

class RSPixel(object):
    """
    遥感图像像素（样本）类
    存储每个像素所有具有的信息
    包括波段信息，在图像中的位置信息，经纬度地理坐标信息和一个ID
    其中ID能够唯一识别
    还存有label信息，label初始为-1
    """
    def __init__(self, id, band_value, x, y, lat, lon, label):
        """
        初始化
        :param bandValue: 像素每个波段的值，是一个numpy.ndarray类型，矩阵
        :param x: 像素在RS图像中的横坐标位置
        :param y: 像素在RS图像中的纵坐标位置
        :return:
        """
        self.__id = id
        self.__lat = lat
        self.__lon = lon
        self.__band = band_value
        self.__x = x
        self.__y = y
        self.__label = label

    @property
    def id(self):
        return self.__id

    @property
    def lat(self):
        return self.__lat

    @property
    def lon(self):
        return self.__lon

    @property
    def band(self):
        return self.__band

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        self.__label = value

    def num_band(self):
        return self.__band.shape[0]

    def insert_label_into_db(self, conn, name):
        """
        将该样本的标记值插入数据库
        :param conn: 数据库链接
        :param name: 遥感图像名称，也是数据库名称
        :return:
        """
        insert_sql = '''INSERT INTO %s_label VALUES (%d, %d, %d, %f, %f, %d)''' % \
                     (name, self.__id, self.__x, self.__y, self.__lat, self.__lon, self.__label)
        conn.execute(insert_sql)
        conn.commit()

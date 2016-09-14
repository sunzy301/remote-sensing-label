# coding=utf-8

import os
import sqlite3

import scipy.io as sio
import numpy as np

from CaffeProject.util.rs_pixel import RSPixel
from CaffeProject.util.parameter import Para
from CaffeProject.util.label_class import GroundTruth

class RSImage(object):
    """
    遥感图像类，包含遥感图像的基本全局信息和所有样本
    """

    def __init__(self, name, dataFileName, labelFileName="", **options):
        # 遥感图像名称
        self._name = name
        self.__id_map = {}

        self._nband = 0
        self._numX = 0
        self._numY = 0

        # 默认读入文件格式是mat
        if "type" not in options.keys():
            options["type"] = "mat"
        # load data from sources
        if options["type"] == "mat":
            # load data from mat file
            # mat文件时ROI文件转成的mat文件
            # mat文件更加方便读入，并且可以在matlab中使用
            self._data = self.load_RS_sample_from_mat(dataFileName)
            if labelFileName != "":
                self._label = self.loadRSLabelFromMat(labelFileName)
            self.dataFileName = dataFileName
            self.labelFileName = labelFileName
        if options["type"] == "csv":
            # load file from csv file
            # csv文件是envi产生的ROI文件
            pass
        # create label tables
        # 在整个对象存在期间保存这个链接，反复链接非常耗费时间
        # 需要在析构对象的时候关闭数据库链接
        self._conn = sqlite3.connect(Para.db_name)
        self.create_label_table()
        ground_truth = GroundTruth()
        # 将类别信息插入数据库
        # 只在创建的时候插入一下，因为测试所以不运行该语句
        # ground_truth.insert_into_table(self._conn, self._name)
        # 从数据库中读入label
        self._label = [0 for i in range(len(self._data))]
        self.load_RS_label_from_db(self._name, self._conn)



        # RGB bands
        if "RGB" in options.keys():
            self._RGBBands = options["RGB"]
        else:
            self._RGBBands = range(3)

    @property
    def name(self):
        """
        遥感图像的名字
        需要按照这个名字存储数据库
        :return:
        """
        return self._name

    @property
    def data(self):
        """
        data是一个list类型，里面包含了所有的像素
        每个像素的波段特征，位置，标记都在RSPixel中
        :return: List[RSPixel]
        """
        return self._data

    @property
    def label(self):
        """
        label是一个ndarray矩阵，包含了所有的标记信息
        单独拿出来是为了之后区分是否有标记方便
        :return:
        """
        return self._label

    @property
    def id_map(self):
        """
        一个map映射
        key是rspixel的id，value是这个rspixel在data中的位置
        :return:
        """
        return self.__id_map

    @property
    def numX(self):
        return self._numX

    @property
    def numY(self):
        return self._numY

    @property
    def nband(self):
        return self._nband

    @property
    def RGBBands(self):
        return self._RGBBands

    @property
    def db_conn(self):
        return self._conn

    def load_RS_sample_from_mat(self, dataFileName, **options):
        """
        读入遥感样本数据文件，文件格式是mat

        文件的标准格式如下：
        ID，X，Y，Lat，Lon，波段1-nband
        ID代表样本编号
        X是样本在图像中的横坐标
        Y是样本在图像肿的纵坐标
        Lat纬度
        Lon是经度
        上述五个维度每个文件都必须有
        后面是nband个波段的数值，数值是原始信息，没有经过处理

        其中矩阵的名称默认就是文件名;如果不是，需要在options中指明
        :param dataFileName: 文件地址
        :param options:可选项
            matrix_name 矩阵名称
        :return:List[RSPixel]
        """
        raw_mat = sio.loadmat(dataFileName)
        if "matrix_name" not in options:
            _, file_name = os.path.split(dataFileName)
            matrix_name = file_name.split(".")[0]
        else:
            matrix_name = options["matrix_name"]
        size_array = raw_mat[matrix_name].shape
        # 波段数量
        nband = size_array[1] - 5
        self._nband = nband
        length = size_array[0]
        # normalize
        maximum_band_matrix = np.tile(raw_mat[matrix_name][:, 5:].max(0), (length, 1))
        minimum_band_matrix = np.tile(raw_mat[matrix_name][:, 5:].min(0), (length, 1))
        raw_mat[matrix_name][:, 5:] = (raw_mat[matrix_name][:, 5:] - minimum_band_matrix) \
                                      /(maximum_band_matrix - minimum_band_matrix + 0.0)# 0.0 for py 2.7
        baseline_x = raw_mat[matrix_name][:, 1].min(0)
        baseline_y = raw_mat[matrix_name][:, 2].min(0)
        maximum_x = raw_mat[matrix_name][:, 1].max(0)
        maximum_y = raw_mat[matrix_name][:, 2].max(0)

        self._numX = int(maximum_x - baseline_x + 1)
        self._numY = int(maximum_y - baseline_y + 1)
        # 产生图像所有的像素数据
        sample_data = list(range(length))
        for i in range(length):
            temp_row = raw_mat[matrix_name][i, :]
            # ID, band, x, y, lat, lon, label
            sample_data[i] = RSPixel(temp_row[0], temp_row[5: 5 + nband],
                                     temp_row[1] - baseline_x, temp_row[2] - baseline_y,
                                     temp_row[3], temp_row[4], -1)
            self.__id_map[int(temp_row[0])] = i
        return sample_data

    def load_RS_label_from_mat(self, labelFileName, **options):
        """
        读入遥感标记数据文件，文件格式是mat
        :param labelFileName: 文件地址
        :param options: 可选项
        :return: ndarray
        """
        pass

    def load_RS_label_from_db(self, name, conn):
        """
        从数据库中读取标记
        根据name，在数据库中寻找 "%s_label" % self._name表
        从中读取当前所有的标记值
        :param name: 遥感图像名称，也是任务名称，用于区分
        :param name: sqlite数据库链接
        :return:
        """
        select_sql = '''select ID, LABEL from %s_label''' % name
        cursor = conn.execute(select_sql)

        for row in cursor:
            temp_id = row[0]+1
            temp_label = row[1]
            temp_index = self.__id_map[temp_id]
            self._data[temp_index].label = temp_label
            self._label[temp_index] = temp_label


    def create_label_table(self):
        """
        每一个遥感图像对应两张表，一张Label的含义，一张存储其label值

        label含义表格表名格式："%s_label_name" % self._name
        label含义表格式如下：
        id, name

        label值表格表名格式： "%s_label" % self._name
        label值表的格式如下：
        ID，X，Y，Lat，Lon，Label
        :return:
        """

        # create label_name table
        create_table_sql_1 = '''CREATE TABLE IF NOT EXISTS %s_label_name
            (ID INT PRIMARY KEY     NOT NULL,
            NAME            TEXT    NOT NULL);''' % self._name
        print(create_table_sql_1)
        self._conn.execute(create_table_sql_1)
        # create label table
        create_table_sql_2 = '''CREATE TABLE IF NOT EXISTS %s_label
            (ID INT PRIMARY KEY     NOT NULL,
            X   INT                 NOT NULL,
            Y   INT                 NOT NULL,
            LAT REAL                NOT NULL,
            LON REAL                NOT NULL,
            LABEL INT               NOT NULL);''' % self._name
        print(create_table_sql_2)
        self._conn.execute(create_table_sql_2)
        self._conn.commit()

    def __del__(self):
        """
        析构函数，释放数据库资源
        :return:
        """
        self._conn.close()

    def load_RS_image_from_mat(self, dataFileName, labelFileName, options):
        """
        旧版本函数，仅用于测试
        根据文件地址读取遥感图像，并根据配置信息进行一定的预处理
        :param fileName:
        :return: List[RSPixel]
        """
        # load mat file
        data = sio.loadmat(dataFileName)
        label = sio.loadmat(labelFileName)
        sizeArray = data["paviaU"].shape
        nx = sizeArray[0]
        ny = sizeArray[1]
        self._numX = nx
        self._numY = ny
        nband = sizeArray[2]
        self._nband = nband
        # reshape
        dataArray = data["paviaU"].reshape(nx*ny, nband)
        # normalize
        maxx = np.tile(dataArray.max(0), (nx*ny, 1))
        minn = np.tile(dataArray.min(0), (nx*ny, 1))
        # +0.0 for both py 2.7.x and 3.x
        dataArray = (dataArray-minn)/(maxx-minn+0.0)
        label = label["paviaU_gt"].reshape(nx*ny, 1)

        data = list(range(nx*ny))
        for i in range(nx*ny):
            tempX = i // ny
            tempY = i-(tempX*ny)
            # bandValue 是一个ndarray类型矩阵
            data[i] = RSPixel(dataArray[i, :], tempX+1, tempY+1, label[i])



        # x,y location on the RS image
        # x = tile(arange(nx), (ny, 1)).T
        # y = tile(arange(ny), (nx, 1))
        # return data, label


def main():
    RSI = RSImage("GF2_Shanghai", "E:\\temp\\rs\\ROI.mat")
    print(len(RSI.data))
    print(RSI.data[0])
    # map test
    print(RSI.data[RSI.id_map[1]].label)
    print(RSI.data[RSI.id_map[2]].label)
    print(RSI.data[RSI.id_map[3]].label)

    print(len(RSI.label))
    # for i in range(10):
    #     print(RSI.label[i])


if __name__ == "__main__":
    main()
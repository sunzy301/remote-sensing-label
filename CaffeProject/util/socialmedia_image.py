# coding=utf-8
# 社交网络图片类
import numpy as np
from PIL import Image

class SMImage(object):
    def __init__(self, id, filename):
        """
        初始化
        :param id:图像的编号
        :param filename: 图像的文件地址
        :return:
        """
        self.__id = id
        self.__filename = filename
        self.__imageArray = None
        self.__feature = None

    @property
    def id(self):
        return self.__id

    @property
    def filename(self):
        return self.__filename

    @property
    def imageArray(self):
        return self.__imageArray

    @imageArray.setter
    def imageArray(self, value):
        self.__imageArray = value


    # 使用某种方法从源图像中提取的整体特征
    # 特征为numpy中的array矩阵
    @property
    def feature(self):
        return self.__feature

    @feature.setter
    def feature(self, value):
        self.__feature = value

    def get_image_array(self):
        """
        取得文件地址对应的图像矩阵，已经做过resize
        :return:
        """
        self.__imageArray = get_imageArray_from_file(self.__filename, resize=1, size=(256, 256))

    def get_image(self):
        """
        取得文件地址对应的图像
        :return:
        """
        return get_image_from_file(self.__filename)


def get_imageArray_from_file(filename, **kw):
    """
    读取图片，并且返回成array的格式
    :param filename: 要读取的图片所在文件地址
    :param kw: 是否进行resize的参数
    :return: 返回resize之后数据的array矩阵
    """
    im = get_image_from_file(filename)
    # resize
    if ("resize" in kw) and (kw["resize"] == 1):
        im = im.resize(kw["size"])
        # im.show()
    imArray = np.array(im)
    return imArray

def get_image_from_file(filename, debug = 0):
    """
    读取图片
    :param filename: 图像所在文件地址
    :param debug:debug参数，如果为1，则会显示图片，仅用于调试
    :return:
    """
    im = Image.open(filename)
    if debug == 1:
        im.show()
    return im

def main():
    image1 = SMImage(0, "e:\\temp\\rs\\test.jpg")
    print(image1.id, image1.filename)
    image1.get_image_array()
    print(image1.imageArray.shape)

if __name__ == "__main__":
    main()
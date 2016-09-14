# coding=utf-8
# 实验一
# 对于指定的遥感图像，选定一个像素点待标记
# 选取该像素点周围的社交网络照片
# 对于社交网络照片提取特征，并进行聚类
# 展示每个簇的聚类中心照片，提供给人进行标记
# 目的是调整选取范围，以及观察上述方法是否可以给人标记提供帮助

from CaffeProject.util import rs_image
from CaffeProject.crowd_sourcing import label
def label_demo1(rs_image_file_name, x, y):
    """

    :param rs_image_file_name: 遥感文件地址，是一个mat文件
    :param x: 待标记点在遥感图像中横坐标
    :param y: 待标记点在遥感图像中纵坐标
    :return:
    """
    # 读取遥感图像
    rs_image = rs_image(rs_image_file_name)
    # 根据xy，在一维RS图像中找到指定的位置
    index_i = (y-1)*rs_image.numX+x
    # 选取照片，提取特征，聚类，人工标记
    label.label_manually(rs_image, rs_image.data[index_i])



if __name__ == "__main__":
    pass


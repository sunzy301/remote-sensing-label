# coding=utf-8
# 实验目的：测试CNN提取的特征对于图片聚类是否能够产生比较好的效果
# 实验步骤：
# 1.读入一组图片
# 2.使用CNN提取特征
# 3.进行聚类并且给每个簇挑选一个代表图片
# 4.人工评价聚类结果和代表图片

import matplotlib.pyplot as plt

from CaffeProject.util.image_set import ImageSet
from CaffeProject.crowd_sourcing import feature_extraction, image_clustering


def test(dir_name):
    # 空的IS
    image_set = ImageSet()
    # 从一个文件夹中读取图片
    image_set.get_images_from_dir(dir_name)
    # 给CNN提取特征，特征存在IS中
    feature_extraction.cnn_image_extraction(image_set)
    # 聚类并选择出合适的代表图像编号
    k = 3
    selected_images = image_clustering.select_center_of_clusering(image_set, k)
    # show selected_images
    subnum = 100+k*10+1
    for i in range(k):
        image_file_name = image_set._iset[selected_images[i]].filename
        sub = plt.subplot(subnum+i)
        sub.imshow(plt.imread(image_file_name))
    plt.show()

def pltShowTest(dir_name):
    """
    测试plt多个子图显示图片
    :return:
    """
    # 空的IS
    image_set = ImageSet()
    # 从一个文件夹中读取图片
    image_set.get_images_from_dir_2(dir_name)
    num = 9
    subnum = 100+num*10+1
    for i in range(num):
        image_file_name = image_set._iset[i].filename
        sub = plt.subplot(subnum+i)
        sub.imshow(plt.imread(image_file_name))
        sub.axis("off")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    # test()
    # show test
    pltShowTest("E:\\sun2\\图片\\星球大战")
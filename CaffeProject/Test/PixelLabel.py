# coding=utf-8
# 实验目的：验证人工识别社交网络图片可以对于单个像素点进行标记
# 实验过程：
# 1.选定需要标记的像素及其位置
# 2.根据位置确定需要纳入聚类的社交网络照片范围
# 3.读取社交网络照片
# 4.使用CNN提取照片特征
# 5.对于照片进行聚类，并且给每个簇选定一个代表图片
# 6.进行人工标记，并且评估图片中信息是否能够进行精确标记

from CaffeProject.util.rs_image import RSImage
from CaffeProject.util.image_set import ImageSet
from CaffeProject.crowd_sourcing import feature_extraction, crowd_sourcing, image_clustering

def test(data_file_name, label_file_name, x, y):
    # load data and label
    rs_image = RSImage(data_file_name, label_file_name)

    lat, lon = get_coordinate(rs_image, x, y)
    # 空的IS
    image_set = ImageSet()
    # 根据RS坐标获取图像集，包括ID和filename
    image_set.get_social_media_images(lat, lon)

    # 给CNN提取特征，特征存在IS中
    feature_extraction.cnn_image_extraction(image_set)
    # 聚类并选择出合适的代表图像编号
    k = 3
    selected_images = image_clustering.select_center_of_clusering(image_set, k)
    # 已有遥感图像，需要标记的位置，社交照片数据集，每个簇选出来的照片编号，然后进行人工标记
    crowd_sourcing.CrowdSourcingLabel(RSImage, image_set, selected_images, (x, y), None)


def get_coordinate(rs_image, x, y):
    """
    根据遥感图像以及x,y，得到具体的坐标位置
    :param rs_image: 遥感图像
    :param x: 像素在图像中横坐标
    :param y: 像素在图像中纵坐标
    :return:
    """
    return 0, 0


if __name__ == "__main__":
    test()
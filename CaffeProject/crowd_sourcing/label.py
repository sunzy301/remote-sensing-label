# coding=utf-8
# 标记过程
import os

from CaffeProject.crowd_sourcing import feature_extraction, crowd_sourcing, image_clustering
from CaffeProject.machine_learning import Clustering
from CaffeProject.util.image_set import ImageSet
from CaffeProject.util import basic_func, parameter, label_class
from CaffeProject.crowd_sourcing import label_process_info

def get_label_process_info(rs_name, id, x, y, lat, lng, **options):
    """
    根据待标记样本信息，获取标记过程所需要的信息
    主要是周围社交网络照片聚类结果
    以及标记的类别含义
    :param rs_name: 遥感图像名称，需要据此获取rgb照片地址
    :param id:待标记样本id
    :param x:样本在遥感图像中横坐标
    :param y:样本在遥感图像中纵坐标
    :param lat:经度
    :param lng:纬度
    :param options: 参数
                debug: 1代表是调试状态，不适用CNN提取特征，不会启动GPU
    :return: labelProcessInfo对象
    """
    if not ("debug" in options):
        debug = 0
    else:
        debug = options["debug"]

    # 遥感的RGB图像，由初始化过程生成
    # 存储在tmp文件夹下，文件名格式为 "%s_rgb.jpg" % rs_name
    rs_rgb_file_name = os.path.join(parameter.Para.tmp, "%s_rgb.jpg" % rs_name)
    # 标记类别
    label_class_instance = label_class.GroundTruth()
    # 空的IS
    image_set = ImageSet("%s_%d" % (rs_name, id))
    # 根据RS坐标(经度，纬度)获取图像集，包括ID和filename
    image_set.get_social_media_images_from_db(lat, lng)
    # 给CNN提取特征，特征存在IS中
    if debug == 1:
        feature_extraction.extract(image_set)
    else:
        feature_extraction.cnn_image_extraction(image_set)
    # 聚类并选择出合适的代表图像编号
    k = 5
    # 聚类结果中的代表性图像编号，格式是List[Int],为id的列表
    selected_images = image_clustering.select_center_of_clusering(image_set, k)
    selected_images_file_name_dict = {}
    for image_id in selected_images:
        selected_images_file_name_dict[image_id] = image_set.image_set[image_id].filename
    # 构建labelProcessInfo对象
    res = label_process_info.labelProcessInFo(rs_name, x, y, rs_rgb_file_name, k,
                                              selected_images_file_name_dict, label_class_instance.GTClass)
    return res

def label_manually(RSImage, unlabeled_set):
    """
    手动标记，用于GUI
    在web版本中不用
    :param RSImage:
    :param unlabeled_set: List[RSPixel]
    :return: no return，直接标注在RSPixel中
    """
    # number of unlabeled samples
    num_unlabel_samples = len(unlabeled_set)
    # crowdsourcing label for each samples
    for i in range(num_unlabel_samples):
        x, y = unlabeled_set[i].x, unlabeled_set[i].y
        # 空的IS
        image_set = ImageSet()
        # 根据RS坐标获取图像集，包括ID和filename
        image_set.get_social_media_images(x, y)
        # 给CNN提取特征，特征存在IS中
        feature_extraction.cnn_image_extraction(image_set)
        # 聚类并选择出合适的代表图像编号
        k = 3
        selected_images = image_clustering.select_center_of_clusering(image_set, k)
        # 已有遥感图像，需要标记的位置，社交照片数据集，每个簇选出来的照片编号，然后进行人工标记
        crowd_sourcing.CrowdSourcingLabel(RSImage, image_set, selected_images, (x, y), unlabeled_set[i])


def label_auto(unlabeled_set):
    """
    在模拟实验中基于已有的标记进行自动标记
    :param unlabeled_set: 被挑选出的需要标记的样本
    :return: 样本的标记类别
    """
    return basic_func.listSelectLabel(unlabeled_set)

def main():
    label_process_info_instance = get_label_process_info("GF2_shanghai", 1, 1, 1, 31.242, 121.497, debug=1)
    label_process_info_json = label_process_info.label_process_info_to_json(label_process_info_instance)
    print(label_process_info_json)

if __name__ == "__main__":
    main()

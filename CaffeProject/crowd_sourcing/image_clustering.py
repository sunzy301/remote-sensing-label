# coding=utf-8
# 图像聚类

from CaffeProject.machine_learning import Clustering
from numpy import *
from CaffeProject.util.image_set import ImageSet
from CaffeProject.util.socialmedia_image import SMImage
from CaffeProject.crowd_sourcing import feature_extraction
from CaffeProject.util import distance
def image_cluster(imageSet, k):
    """
    使用经过cnn或者其他方法提取的特征，使用kmeans进行聚类
    :param imageSet: 图像照片数据集，已经对已每张图片提取过特征
    :return: 聚类结果
    """
    featureSet = [i for i in range(len(imageSet.image_set))]
    for i in range(len(imageSet.image_set)):
        featureSet[i] = imageSet.image_set[i].feature
    featureArray = hstack(tuple(featureSet)).T
    label, centers = Clustering.clustering(featureArray, k=k)
    return label, centers

def select_center_of_clusering(imageSet, k):
    """
    对于聚类之后的结果，给每个类选择一个距离聚类中心最近的图片作为代表性样本
    :param imageSet:
    :param k:
    :return:List[Int]
            代表图片的编号ID，每个簇有一个代表图片
    """
    clusteringResult, centers = image_cluster(imageSet, k)
    image_ceneter = [i for i in range(k)]
    for i in range(k):
        min = 1<<31
        for j in range(len(clusteringResult)):
            if clusteringResult[j] == i:
                d = distance.euclideanDistance(imageSet.image_set[j].feature, centers[i])
                if d < min:
                    min = d
                    image_ceneter[i] = j
    return image_ceneter




if __name__ == "__main__":
    dirname = "E:\\sun2\\工作\\python\\CaffeProject\\CaffeProject\\Crawler\\data\\hello"
    IS = ImageSet()
    IS.get_images_from_dir(dirname)
    feature_extraction.extract(IS)
    # clusteringResult, centers = image_cluster(IS, 3)
    # print(clusteringResult, centers.shape)
    centers = select_center_of_clusering(IS, 3)
    print(centers)
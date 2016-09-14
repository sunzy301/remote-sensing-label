# coding=utf-8
# 在oxford5k数据集中构建子集，对其进行聚类操作
# 分析聚类结果

import random
import os

import numpy
from sklearn import decomposition

from CaffeProject.machine_learning import Clustering
from CaffeProject.util import distance

def construct_data_sets(names_file_name, dir_name, main_cluster_id, alpha):
    """

    :param names_file_name: 图像名称存储的地址
    :param dir_name: 特征向量存储的文件夹
    :return:
    """
    pca = get_pca(dir_name)
    query_name = ["all_souls", "ashmolean", "balliol", "bodleian", "christ_church", "cornmarket",
              "hertford", "jesus", "keble", "magdalen", "new", "oriel", "oxford", "pitt_rivers", "radcliffe_camera", "trinity", "worcester"]
    file_names = []
    with open(names_file_name, "r") as f:
        for str in f.readlines():
            # print(str.strip())
            file_names.append(str.strip())
    # 主聚类类别编号，从0到16，一共17个选择性
    main_cluster_id = main_cluster_id
    main_cluster_names = []
    other_names = []
    for str_name in file_names:
        if str_name.find(query_name[main_cluster_id]) >= 0:
            main_cluster_names.append(str_name)
        else:
            other_names.append(str_name)
    print(len(main_cluster_names), len(other_names))
    # 其余类的样本数量总和
    num_other_images = int(len(main_cluster_names)*alpha)
    slice_other_names = random.sample(other_names, num_other_images)
    main_cluster_names.extend(slice_other_names)
    print(len(main_cluster_names))
    feature_vectors = []
    # 读取特征
    for str_name in main_cluster_names:
        temp_feature_vector = numpy.load(os.path.join(dir_name, str_name+".jpg.npy"))#[384:]
        temp_feature_vector = pca.transform(temp_feature_vector.T)
        print(temp_feature_vector.shape)
        feature_vectors.append(normalize(temp_feature_vector.T).T)

    feature_vectors = numpy.vstack(tuple(feature_vectors))
    print(feature_vectors.shape)
    # clustering
    k = 5
    label, centers = Clustering.clustering(feature_vectors, k=k)
    # for i in range(len(main_cluster_names)):
    #     print(main_cluster_names[i], label[i])


    # select center
    image_center = [i for i in range(k)]
    for i in range(k):
        min = 1<<31
        for j in range(len(main_cluster_names)):
            if label[j] == i:
                d = distance.euclideanDistance(feature_vectors[j], centers[i])
                if d < min:
                    min = d
                    image_center[i] = j
    print("\n\ncenters")
    cluster_centers = []
    for i in range(k):
        print(main_cluster_names[image_center[i]])
        cluster_centers.append(main_cluster_names[image_center[i]])

    for i in range(k):
        nums = [0]*17
        for j in range(len(main_cluster_names)):
            if label[j] == i:
                for kk in range(17):
                    if main_cluster_names[j].find(query_name[kk]) >= 0:
                        nums[kk] += 1
                        break
        print(i, nums)
    return cluster_centers


def get_pca(dir_name):
    """
    通过所有样本的特征计算得到pca变化矩阵
    :param dir_name:
    :return: 返回一个scikit的pca对象
    """
    feature_vectors = []
    for str_name in os.listdir(dir_name):
        temp_feature_vector = numpy.load(os.path.join(dir_name, str_name))
        feature_vectors.append(normalize(temp_feature_vector))
    feature_vectors = numpy.vstack(tuple(feature_vectors))
    print(feature_vectors.shape)
    pca = decomposition.PCA(n_components=128)
    new_feature_vectors = pca.fit_transform(feature_vectors)
    print(new_feature_vectors.shape)
    return pca

def normalize(vector):
    """
    正则化
    :param vector:
    :return:
    """
    import math
    num = vector.shape[0]
    sum = 0
    for i in range(num):
        sum += vector[i]*vector[i]
    sum = math.sqrt(sum)
    result_vec = numpy.zeros(vector.shape)
    for i in range(num):
        result_vec[i] = vector[i]/sum
    return  result_vec

if __name__ == "__main__":
    construct_data_sets("E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\oxford5k_names.txt", "E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\features")

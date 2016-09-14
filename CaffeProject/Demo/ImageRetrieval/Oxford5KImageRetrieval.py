# coding=utf-8
# 用于图像检索实验
# 找到实验图片的ranked list，然后和标记值进行比对

import os
import math

import numpy
from sklearn import decomposition


def image_retrieval(features_dir_name, gt_dir_name):
    # 读取所有图像的特征，并且对其做PCA与正则化
    feature_vectors = []
    total_names = []
    for str_name in os.listdir(features_dir_name):
        split = str_name.split(".")
        total_names.append(split[0])
        # print(str_name)
        temp_feature_vector = numpy.load(os.path.join(features_dir_name, str_name))
        print(temp_feature_vector)
        feature_vectors.append(temp_feature_vector)
    feature_vectors = numpy.vstack(tuple(feature_vectors))
    print(feature_vectors.shape, type(feature_vectors))
    pca = decomposition.PCA(n_components=128)
    # new_feature_vectors = pca.fit_transform(feature_vectors)
    new_feature_vectors = feature_vectors
    print(new_feature_vectors.shape)
    feature_vectors = []
    for i in range(new_feature_vectors.shape[0]):
        feature_vectors.append(normalize(new_feature_vectors[i, :]))
    print(len(feature_vectors), feature_vectors[0].shape)
    # print(feature_vectors[0])
    # return
    query_name = ["all_souls", "ashmolean", "balliol", "bodleian", "christ_church", "cornmarket",
              "hertford", "keble", "magdalen", "pitt_rivers", "radcliffe_camera"]
    query_num = [1, 2, 3, 4, 5]
    # 要查询的图片的具体名称，比如all_souls_5
    image_file_names = []
    # 要查询的图片的编号，比如all_souls_1
    query_id = []
    for qname in query_name:
        for qnum in query_num:
            query_file_name = qname+"_"+("%d" % qnum)
            with open(os.path.join(gt_dir_name, query_file_name+"_query.txt")) as f:
                words = f.readline().split(" ")
                image_file_names.append(words[0][5:])
                query_id.append(qname+"_"+("%d" % qnum))
    print(image_file_names)
    print(query_id)
    n = 0
    mAPs = [0]*len(image_file_names)
    for name in image_file_names:
        i = total_names.index(name)
        print(i)
        # 计算query与数据库中每张图片之间距离
        query_feature = feature_vectors[i]
        d = [0]*len(feature_vectors)
        for j in range(len(feature_vectors)):
            d[j] = distance(query_feature, feature_vectors[j])
        # 对于距离进行排序
        d_with_key = list(zip(d, list(range(len(d)))))
        # print(d_with_key)
        d_with_key = sorted(d_with_key, key=lambda x: x[0])
        print(d_with_key)

        # 根据gt计算mAP
        alpha = 0.5
        positive_list, negative_list = load_gt(gt_dir_name, query_id[n])
        query_result_list = []
        for j in range(len(d_with_key)):#len(positive_list)+len(negative_list)):
            if d_with_key[j][0] < alpha:
                query_result_list.append(total_names[d_with_key[j][1]])
            else:
                break
        # print(query_result_list, len(query_result_list))
        # print(positive_list)
        mAP = get_mAP(query_result_list, positive_list, negative_list)
        print(mAP)
        mAPs[n] = mAP
        n += 1
    print(mAPs)
    avgmAp = sum(mAPs)/len(mAPs)
    print(avgmAp)


def get_mAP(query_list, good_List, bad_list):
    """
    计算查询的mAP，平均精确度
    :param query_list: 查询得到的ranked list
    :param good_List: 正样本集合
    :param bad_list: 负样本集合
    :return:
    """
    old_precision = 0
    old_recall = 0

    ap = 0
    p = 0
    intersect_size = 0
    for i in range(len(query_list)):
        if query_list[i] in bad_list:
            continue
        if query_list[i] in good_List:
            intersect_size += 1
        recall = intersect_size / len(good_List)
        precision = intersect_size / (p+1)
        ap += (recall - old_recall)*((old_precision + precision)/2.0)

        old_recall = recall
        old_precision = precision

        p += 1

    return ap

def load_gt(dir_name, query_name):
    """
    读取gt
    :param dir_name:
    :param query_name:
    :return: positive_list 正样本集; negative_list 负样本集
    """
    positive_list = []
    with open(os.path.join(dir_name, query_name+"_good.txt")) as f:
        for str_name in f.readlines():
            positive_list.append(str_name.strip())
    with open(os.path.join(dir_name, query_name+"_ok.txt")) as f:
        for str_name in f.readlines():
            positive_list.append(str_name.strip())
    negative_list = []
    with open(os.path.join(dir_name, query_name+"_junk.txt")) as f:
        for str_name in f.readlines():
            negative_list.append(str_name.strip())
    return positive_list, negative_list

def distance(vector1, vector2):
    """
    计算两个向量之间距离
    考虑欧式距离或者cos夹角
    :param vector1: 向量1
    :param vector2: 向量2
    :return: 距离
    """
    if len(vector1) != len(vector2):
        return -1
    sumV = 0
    # Euclidean Distance
    for i in range(len(vector1)):
        sumV += (vector1[i]-vector2[i])*(vector1[i]-vector2[i])
    sumV = math.sqrt(sumV)
    return sumV

    # Cosine
    # up = 0
    # down1, down2 = 0, 0
    # for i in range(len(vector1)):
    #     up += vector1[i]*vector2[i]
    #     down1 += vector1[i]**2
    #     down2 += vector2[i]**2
    # return up/(math.sqrt(down1)*math.sqrt(down2))

    # for i in range(len(vector1)):
    #     sumV += vector1[i]*vector2[i]
    # return sumV

    #



def normalize(vector):
    """
    正则化
    :param vector:
    :return:
    """
    num = vector.shape[0]
    sum = 0
    for i in range(num):
        sum += vector[i]*vector[i]
    print(vector)
    print(vector.shape, vector[2])
    sum = math.sqrt(sum)
    result_vec = numpy.zeros(vector.shape)
    for i in range(num):
        result_vec[i] = vector[i]/sum
    return result_vec

if __name__ == "__main__":
    # image_retrieval("E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\newfeatures", "E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\gt")
    image_retrieval("/usr/caffe/caffe-master/examples/image_retrieval/features", "/usr/caffe/caffe-master/examples/image_retrieval/gt")
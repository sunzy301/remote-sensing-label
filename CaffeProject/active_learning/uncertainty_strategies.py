# coding=utf-8
# uncertainty strategies
import numpy as np
from numpy import *
def ms(distance):
    """
    使用MS策略计算不确定度，即根据每个样本距离最近的分类平面距离进行排序
    寻找距离最小的样本，认为其具有最高的不确定度
    :param distance: 每个样本距离到分类平面的距离（默认其实one-vs-all策略的多分类器）
    :return: 经过排序的最小距离，以及在unlabeled_pool中的序号
    """
    min_distance = abs(distance).min(1)
    index = np.argsort(min_distance)
    sorted_min_distance = min_distance[index]
    return sorted_min_distance, index


def mclu(distance):
    """
    使用MCLU策略计算不确定度，即根据样本最小的两个到分类平面的距离的距离差进行排序
    距离差越小，认为其具有越高的不确定度
    :param distance: 每个样本距离到分类平面的距离（默认其实one-vs-all策略的多分类器）
    :return: 经过排序的最小距离差，以及在unlabeled_pool中的序号
    """
    distance = np.sort(distance, 1)
    min_distance = distance[:, -1]-distance[:, -2]
    index = np.argsort(min_distance)
    sorted_min_distance = min_distance[index]
    return sorted_min_distance, index

def rand(distance):
    """
    对于样本随机排序
    :param distance: 每个样本距离到分类平面的距离（默认其实one-vs-all策略的多分类器）
    :return: 返回随机排序之后的距离（无用），以及随机排序序号
    """
    index = arange(distance.shape(0))
    random.shuffle(index)
    return distance[index, 1], index

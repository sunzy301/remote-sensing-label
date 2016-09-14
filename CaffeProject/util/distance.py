# coding=utf-8
# for distance measurement
from numpy import *
def euclideanDistance(victor1, victor2):
    """
    欧氏距离，输入是两个numpy的array矩阵
    :param victor1: 向量1
    :param victor2: 向量2
    :return: 距离
    """
    if len(victor1) != len(victor2):
        return -1
    Dsum = 0
    for i in range(victor1.shape[0]):
        Dsum += (victor1[i]-victor2[i])*(victor1[i]-victor2[i])
    Dsum = sqrt(Dsum)
    return Dsum

if __name__ == "__main__":
    a1 = array([1, 2])
    a2 = array([4, 6])
    print(euclideanDistance(a1, a2))
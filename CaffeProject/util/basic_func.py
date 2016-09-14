# coding=utf-8
# 一些基础函数
from numpy import *
from CaffeProject.util.rs_image import RSImage
import math


def list2ndarray(listRSPixel):
    """
    从list[RSPixel]转为两个矩阵，一个是bandValue，另一个是label
    :param listRSPixel:
    :return:
    """
    nx = len(listRSPixel)
    ny = listRSPixel[0].band.shape[0]
    dataArray = zeros((nx, ny))
    labelArray = zeros((nx, 1))
    for i in range(nx):
        dataArray[i, :] = listRSPixel[i].band
        labelArray[i] = listRSPixel[i].label
    return dataArray, labelArray

def listSelectLabel(listRSPixel):
    """
    从list[RSPixel]中提取label矩阵
    :param listRSPixel:
    :return:
    """
    nx = len(listRSPixel)
    ny = listRSPixel[0].band.shape[0]
    labelArray = zeros((nx, 1))
    for i in range(nx):
        labelArray[i] = listRSPixel[i].label
    return labelArray

def rad(d):
    return d*math.pi/180.0

def distanceEarth(lat1, lon1, lat2, lon2):
    """
    返回两个经纬度在地球表面的精确距离
    :param lat1: 经度一
    :param lon1: 纬度一
    :param lat2: 经度二
    :param lon2: 纬度二
    :return: 距离值 单位是千米
    """
    EARTH_RADIUS = 6378.137
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1-radLat2
    b = rad(lon1)-rad(lon2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2), 2)))
    s = s * EARTH_RADIUS
    # s = math.round(s * 10000) / 10000
    s = round(s*10000)/10000
    return s

if __name__ == "__main__":
    print(distanceEarth(117.60972, 24.118418, 117.6113, 24.11931))
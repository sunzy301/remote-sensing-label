# coding=utf-8
# 实验0
# 实验数据集为Oxford5K
# 没有地理坐标信息，指定待标记样本位置
# 遥感图像使用google地图卫星照片
# 模拟生成社交网络照片数据集

import os
import sys

from PyQt4 import QtGui

from CaffeProject.Demo.PIEEE import ClusterDemo1
from CaffeProject.GUI import LabelWindow

def label_demo0(names_file_name, feature_dir_name, data_dir_name):
    cluster_centers = ClusterDemo1.construct_data_sets(names_file_name, feature_dir_name, 9, 2)
    print(cluster_centers)
    for i in range(len(cluster_centers)):
        cluster_centers[i] = os.path.join(data_dir_name, cluster_centers[i])
    rs_image_file_name = "E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\oxford_magdalen.png"
    app = QtGui.QApplication(sys.argv)
    widget = LabelWindow.LabelWindow(rs_image_file_name, cluster_centers, None)
    widget.show()
    app.exec_()

if __name__ == "__main__":
    label_demo0("E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\oxford5k_names.txt",
                "E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\features",
                "E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\data")
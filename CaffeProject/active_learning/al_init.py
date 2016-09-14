# coding=utf-8
# al初始化脚本
# 读入al初始化信息，进行初始化操作，保存al训练信息

import sys
import os

import json

from CaffeProject.active_learning.active_learning import ActiveLearning
from CaffeProject.util.parameter import Para
from CaffeProject.active_learning import al_init_info
from CaffeProject.active_learning import al_train_info

# 初始化参数使用json字符串传入
# json字符串存在tmp文件夹中，名称为 "%s_al_init.json" % rs_name. 其中name是遥感图像名称
al_init_info_file_name = sys.argv[0]
with open(al_init_info_file_name, "r") as f:
    al_init_info_json = f.readline()
# 将字符串转为ALInitInfo
al_init_info_instance = al_init_info.AlInitInfo(al_init_info_json)

al = ActiveLearning()
# 初始化过程，返回al的训练信息ALTrainInfo
al_train_info_instance = al.init_process(al_init_info_instance)

# al训练信息json文件存储地址
# 存储在tmp文件夹中，名称为 "%s_al_train.json" % rs_name.
al_train_info_file_name = os.path.join(Para.tmp, "%s_al_train.json" % al_init_info_instance.rs_name)
# 转为json字符串
al_train_info_json = al_train_info_instance.to_json
# 持久化，保存训练信息json
with open(al_train_info_file_name, "w") as f:
    f.write(al_train_info_json)


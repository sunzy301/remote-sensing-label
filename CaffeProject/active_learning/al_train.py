# coding=utf-8
# al训练脚本
# 读入al训练信息，进行训练操作，保存更新后的al训练信息

import sys
import os

import json

from CaffeProject.active_learning.active_learning import ActiveLearning
from CaffeProject.active_learning import al_train_info
from CaffeProject.util.parameter import Para

# 参数为train_info所在文件地址
# 文件在tmp文件夹下，格式为 "%s_train_info" % rs_name
# 其中rs_name为遥感图像名称
al_train_info_name = sys.argv[0]
with open(al_train_info_name, "r") as f:
    al_train_info_json = f.readline()
# 将json转为AlTrainInfo
al_train_info_instance =  al_train_info.AlTrainInfo(al_train_info_json)

al = ActiveLearning()
# AL训练过程后，更新训练信息
al_train_info_instance_refresh = al.train_process(al_train_info_instance)
# 将ALTrainInfo转为json字符串
al_train_info_json_refresh = al_train_info_instance_refresh.to_json()
# 将json字符串保存到指定的位置
# 文件在tmp文件夹下，格式为 "%s_train_info" % rs_name
# 其中rs_name为遥感图像名称
# 将覆盖原来的训练信息
al_train_info_name_refresh = os.path.join(Para.tmp, "%s_train_info" % al_train_info_instance.rs_name)
with open(al_train_info_name_refresh, "w") as f:
    f.write(al_train_info_json_refresh)
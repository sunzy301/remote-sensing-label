# coding=utf-8
# 标记操作脚本
# Controller发送待标记样本信息
# Model进行操作，并且将产生标记页面需要的信息转为json字符串，保存tmp文件夹中
# 之后Controller读取json文件，生成对应的View
# View得到标记，交给Controller，Controller直接存入数据库

import sys
import os

import json

from CaffeProject.crowd_sourcing import label
from CaffeProject.util.parameter import Para
from CaffeProject.crowd_sourcing import label_process_info

# 标记参数比较简单，不使用json
# 六个参数
# 1. rs_name: 遥感图像名称也是任务名称
# 2. id: 待标记样本编号
# 3. x: 在遥感图像中横坐标位置
# 4. y: 在遥感图像中纵坐标位置
# 5. lat: 经度
# 6. lng: 纬度

if len(sys.argv) != 6:
    print("argv is not right!")
    sys.exit()
else:
    rs_name = sys.argv[0]
    id = int(sys.argv[1])
    x = int(sys.argv[2])
    y = int(sys.argv[3])
    lat = float(sys.argv[4])
    lng = float(sys.argv[5])

# 获取label_process_info
label_process_info_instance = label.get_label_process_info(rs_name, id, x, y, lat, lng)
# 将其转为json字符串，然后存于tmp文件夹中
label_process_info_json = label_process_info.label_process_info_to_json(label_process_info_instance)
# 对于一个特定的待标记样本
# 其存储地址为 "%s_%d_label_info.json" % (rs_name, id).
# 其中rs_name是遥感图像名称，id是样本编号
label_process_info_name = os.path.join(Para.tmp, "%s_%d_label_info.json" % (rs_name, id))
with open(label_process_info_name, "w") as f:
    f.write(label_process_info_json)


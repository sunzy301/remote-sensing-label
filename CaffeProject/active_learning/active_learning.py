# coding=utf-8

import os
import sqlite3
import json

from numpy import *
from scipy.misc import imsave

from CaffeProject.util.rs_image import RSImage
from CaffeProject.util import basic_func
from CaffeProject.util import parameter
from CaffeProject.active_learning import al_train_info
from CaffeProject.active_learning import al_init_info
from CaffeProject.active_learning import AL
class ActiveLearning(object):
    """
    主动学习类
    继承数据读入，al学习，生成待标记样本三个主要功能
    """

    def init_process(self, info):
        """
        active learning初始化过程
        初始化的标记样本由C端生成特殊类型标记页面，标记之后的结果直接存于数据库
        第一次训练时直接从数据库中生成即可。
        :param info: ALInitInfo类
        :return: 返回ALTrainInfo类，al的训练参数信息
        """
        print(type(info))
        # 读入数据
        rs_image = RSImage(info.rs_name, info.data_file_name)
        # 构建遥感的RGB图像
        rgb = info.rgb
        r_band = rgb[0]
        g_band = rgb[1]
        b_band = rgb[2]

        data = basic_func.list2ndarray(rs_image.data)[0]
        data = reshape(data, [rs_image.numX, rs_image.numY, rs_image.nband])
        print(data.shape)
        rgb_image = data[:, :, ix_([r_band, g_band, b_band])]
        rgb_image = reshape(rgb_image, [rs_image.numX, rs_image.numY, 3])

        # print(rgb_image.shape)
        image_save_name = os.path.join(parameter.Para.tmp, "%s.jpg" % info.rs_name)
        imsave(image_save_name, rgb_image)

        # 构建用于初始化训练参数信息ALTrainInfo的json字符串
        al_train_info_json = al_train_info.AlTrainInfo.\
            al_train_info_to_json(info.rs_name, info.data_file_name,
                                  info.label_class_num, info.al_iteration_num,
                                  0, info.batch_size)

        al_train_info_instance = al_train_info.AlTrainInfo(al_train_info_json)
        return al_train_info_instance

    def train_process(self, info):
        """
        active learning训练过程
        :param info: ALTrainInfo类，训练参数信息
        :return: 更新之后的训练参数信息，ALTrainInfo类
        """
        # 读入数据
        rs_image = RSImage(info.rs_name, info.data_file_name)
        nband = rs_image.nband

        # 准备数据
        # 从数据库中读入labeled_sample_set

        conn = rs_image.db_conn
        sql = """SELECT ID, LABEL FROM %s_label""" % info.rs_name
        cursor = conn.execute(sql)
        labeled_dict = dict()
        labeled_sample_index_list = list()
        for row in cursor:
            # row[0] id; row[1] label
            labeled_sample_index_list.append(row[0])
            labeled_dict[row[0]] = row[1]
        # 设置标记的样本值
        # rs_image.id_map[k]是样本ID对应的在list中位置
        # rs_image.data[rs_image.id_map[k]]是一个RSPixel类的实例

        for k, v in labeled_dict.items():
            rs_image.data[rs_image.id_map[k]].label = v

        # 所有ID的列表
        all_id_list = [k for k in rs_image.id_map.keys()]
        # 没有标记的样本列表,长度已经知道
        unlabeled_sample_index_list = [0 for i in range(len(all_id_list)-len(labeled_sample_index_list))]

        # 对于两个个列表进行排序
        sorted(labeled_sample_index_list)
        sorted(all_id_list)

        # 构建unlabeled_sample_index_list
        labeled_i = 0
        unlabeled_i = 0
        len_labeled_index_list = len(labeled_sample_index_list)
        for i in range(len(all_id_list)):
            if all_id_list[i] == labeled_sample_index_list[labeled_i]:
                if labeled_i < len_labeled_index_list - 1:
                    labeled_i += 1
            else:
                unlabeled_sample_index_list[unlabeled_i] = all_id_list[i]
                unlabeled_i += 1

        # 构建实际数据集
        # labeled_sample_list, unlabeled_sample_list
        labeled_sample_list = list(rs_image.data[rs_image.id_map[labeled_sample_index_list[i]]]
                                   for i in range(len(labeled_sample_index_list)))
        unlabeled_sample_list = list(rs_image.data[rs_image.id_map[unlabeled_sample_index_list[i]]]
                                   for i in range(len(unlabeled_sample_index_list)))

        print(len(labeled_sample_list), len(unlabeled_sample_list))
        # 传入AL训练
        # 返回选择的待标记样本ID列表
        selected_sample_list = AL.al_one_step(labeled_sample_list, unlabeled_sample_list, nband, info.batch_size)
        print(selected_sample_list)
        # 将新一轮待标记样本信息存入数据库
        # 在数据库中未标记的样本label值为-1
        values = list()
        for i in selected_sample_list:
            id = i
            index = rs_image.id_map[id]
            x = rs_image.data[index].x
            y = rs_image.data[index].y
            lat = rs_image.data[index].lat
            lng = rs_image.data[index].lon
            label = -1
            temp = (id, x, y, lat, lng, label)
            values.append(temp)
        insert_sql = """INSERT INTO %s_label VALUES(?, ?, ?, ?, ?, ?)""" % info.rs_name
        conn.executemany(insert_sql, values)
        conn.commit()

        # 更新训练参数数据
        # 其中训练迭代当前轮数+1
        al_train_info_json = al_train_info.AlTrainInfo.\
            al_train_info_to_json(info.rs_name, info.data_file_name,
                                  info.label_class_num, info.al_iteration_num,
                                  info.now_iteration_num+1, info.batch_size)

        al_train_info_instance = al_train_info.AlTrainInfo(al_train_info_json)
        return al_train_info_instance






def init_test():
    """
    用于测试初始化过程
    :return:
    """
    init_dict = dict()
    init_dict["rs_name"] = "GF2_shanghai"
    init_dict["data_file_name"] = "E:\\temp\\rs\\ROI.mat"
    init_dict["label_class_num"] = 10
    init_dict["rgb"] = [1, 2, 3]
    init_dict["al_iteration_num"] = 20
    init_dict["batch_size"] = 100
    init_json = json.dumps(init_dict)
    print(init_json)
    init_info_instance = al_init_info.AlInitInfo(init_json)
    al = ActiveLearning()
    al_train_info_instance = al.init_process(init_info_instance)
    al_train_info_json = al_train_info_instance.to_json()
    print(al_train_info_json)

def train_test():
    """
    用于训练过程测试
    :return:
    """
    init_dict = dict()
    init_dict["rs_name"] = "GF2_shanghai"
    init_dict["data_file_name"] = "E:\\temp\\rs\\ROI.mat"
    init_dict["label_class_num"] = 10
    init_dict["rgb"] = [1, 2, 3]
    init_dict["al_iteration_num"] = 20
    init_dict["batch_size"] = 100
    init_json = json.dumps(init_dict)
    print(init_json)
    init_info_instance = al_init_info.AlInitInfo(init_json)
    al = ActiveLearning()

    al_train_info_instance_0 = al.init_process(init_info_instance)
    al_train_info_json = al_train_info_instance_0.to_json()
    print(al_train_info_json)
    print("init success")

    al_train_info_instance_1 = al.train_process(al_train_info_instance_0)
    al_train_info_json = al_train_info_instance_1.to_json()
    print(al_train_info_json)

    al_train_info_instance_2 = al.train_process(al_train_info_instance_0)
    al_train_info_json = al_train_info_instance_2.to_json()
    print(al_train_info_json)

def main():
    train_test()

if __name__ == "__main__":
    main()
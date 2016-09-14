# coding=utf-8

import sys
import json

class AlTrainInfo(object):
    """
    主动学习训练信息类
    每轮AL都需要接受信息进行训练，并且产生更新的训练信息

    before training:
    C -> alTrainInfo -> M
    after training:
    M -> refreshed alTrainInfo -> M

    alTrainInfo:
        rs_name: 遥感图像名称，也是任务名称
        data_file_name: 遥感图像地址
        label_class_num: 标记类别数量
        al_iteration_num: AL迭代轮数
        now_iteration_num: 当前的迭代轮数，初始化时为0，做完一轮训练+1
        batch_size: 每轮选择待标记样本数量
        labeled_num: 已标记数据集样本数量
        candidate_num: 未标记池样本数量
        labeled_id_set: 已标记数据集样本编号集合，
                        是一个List[Int]，存储所有已标记样本ID
                        不再这个集合中的样本都是未标记的

    使用json字符串作为输入初始化对象
    需要将对象转为json字符串，为之后保存准备
    """

    def __init__(self, json_str):
        """
        使用json字符串进行初始化
        会进行参数检查
        :param json_str:json字符串
        :return:
        """
        info_dict = json.loads(json_str)
        self.__rs_name = self.__check(info_dict, "rs_name")
        self.__data_file_name = self.__check(info_dict, "data_file_name")
        self.__label_class_num = self.__check(info_dict, "label_class_num")
        self.__al_iteration_num = self.__check(info_dict, "al_iteration_num")
        self.__now_iteration_num = self.__check(info_dict, "now_iteration_num")
        self.__batch_size = self.__check(info_dict, "batch_size")
        # self.__labeled_num = self.__check(info_dict, "labeled_num")
        # self.__candidate_num = self.__check(info_dict, "candidate_num")
        # self.__labeled_id_set = self.__check(info_dict, "labeled_id_set")

    @classmethod
    def al_train_info_to_json(cls, rs_name_p, data_file_name_p, label_class_num_p,
                     al_iteration_num_p, now_iteration_num_p, batch_size_p):
        """
        使用各个项的值生成一个可以用于初始化的json字符串
        是一个静态方法
        :param rs_name_p:
        :param data_file_name_p:
        :param label_class_num_p:
        :param al_iteration_num_p:
        :param now_iteration_num_p:
        :param batch_size_p:
        :return: 一个json字符串，可以直接用于初始化ALTrainInfo类
        """
        info_dict = dict()
        info_dict["rs_name"] = rs_name_p
        info_dict["data_file_name"] = data_file_name_p
        info_dict["label_class_num"] = label_class_num_p
        info_dict["al_iteration_num"] = al_iteration_num_p
        info_dict["now_iteration_num"] = now_iteration_num_p
        info_dict["batch_size"] = batch_size_p
        return json.dumps(info_dict)

    def __check(self, info_dict, name):
        """
        通用化的参数检查函数
        如果参数字典中不存在这个项，就会报错并且退出程序
        :param info_dict: 参数字典
        :param name: 参数名称
        :return: 参数内容
        """
        if name not in info_dict:
            print("Wrong:", name, " does not exist in al_train_info")
            sys.exit()
        else:
            return info_dict[name]

    def to_json(self):
        """
        根据自身对象生成json字符串
        :return: json字符串
        """
        info_dict = dict()
        info_dict["rs_name"] = self.__rs_name
        info_dict["data_file_name"] = self.__data_file_name
        info_dict["label_class_num"] = self.__label_class_num
        info_dict["al_iteration_num"] = self.__al_iteration_num
        info_dict["now_iteration_num"] = self.__now_iteration_num
        info_dict["batch_size"] = self.__batch_size
        # info_dict["labeled_num"] = self.__labeled_num
        # info_dict["candidate_num"] = self.__candidate_num
        # info_dict["labeled_id_set"] = self.__labeled_id_set

        return json.dumps(info_dict)

    @property
    def rs_name(self):
        return self.__rs_name

    @property
    def data_file_name(self):
        return self.__data_file_name

    @property
    def label_class_num(self):
        return self.__label_class_num

    @property
    def al_iteration_num(self):
        return self.__al_iteration_num

    @property
    def now_iteration_num(self):
        return self.__now_iteration_num

    @property
    def batch_size(self):
        return self.__batch_size

    @property
    def labeled_num(self):
        return self.__labeled_num

    @property
    def candidate_num(self):
        return self.__candidate_num

    @property
    def labeled_id_set(self):
        return self.__labeled_id_set

def main():
    pass

if __name__ == "__main__":
    main()




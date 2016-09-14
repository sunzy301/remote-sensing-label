# coding=utf-8
import sys
import json

class AlInitInfo(object):
    """
    主动学习初始化信息类
    由Controller传给Model
    init:
        C -> alInitInfo -> M
        alInitInfo:
            rs_name: 遥感图像名称，也是任务名称
            data_file_name: 遥感图像地址
            rgb: rgb三个波段的数值 List[int]，第一是R，第二是G，第三是B
            label_class_num: 标记类别数量
            init_num_per_class: 每个类别的初始标记数量
            al_iteration_num: AL迭代轮数
            batch_size: 每轮选择待标记样本数量
            #candidate_num: 未标记池样本数量，默认为所有样本，不设置该值
            #validation_set_num: 验证集样本数量，实际中由于没有标记，可以设置为0

    初始化输入为json字符串
    init信息类只会在初始化操作中使用一次，没有输出的通道
    """

    def __init__(self, json_str):
        """
        使用json字符串初始化
        会进行参数检查
        :param json: json字符串
        :return:
        """
        info_dict = json.loads(json_str)
        self.__rs_name = self.__check(info_dict, "rs_name")
        self.__data_file_name = self.__check(info_dict, "data_file_name")
        self.__label_class_num = self.__check(info_dict, "label_class_num")
        # self.__init_num_per_class = self.__check(info_dict, "init_num_per_class")
        self.__rgb = self.__check(info_dict, "rgb")
        self.__al_iteration_num = self.__check(info_dict, "al_iteration_num")
        self.__batch_size = self.__check(info_dict, "batch_size")
        # self.__candidate_num = self.__check(info_dict, "candidate_num")


    def __check(self, info_dict, name):
        """
        通用化的参数检查函数
        如果参数字典中不存在这个项，就会报错并且退出程序
        :param info_dict: 参数字典
        :param name: 参数名称
        :return: 参数内容
        """
        if name not in info_dict:
            print("Wrong:", name, " does not exist in al_init_info")
            sys.exit()
        else:
            return info_dict[name]

    @property
    def rs_name(self):
        return self.__rs_name

    @property
    def data_file_name(self):
        return self.__data_file_name

    @property
    def rgb(self):
        return self.__rgb

    @property
    def label_class_num(self):
        return self.__label_class_num

    @property
    def init_num_per_class(self):
        return self.__init_num_per_class

    @property
    def candidate_num(self):
        return self.__candidate_num

    @property
    def al_iteration_num(self):
        return self.__al_iteration_num

    @property
    def batch_size(self):
        return self.__batch_size
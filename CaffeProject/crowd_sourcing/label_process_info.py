# coding=utf-8

import json

from CaffeProject.util.label_class import GroundTruth

class labelProcessInFo(object):
    """
    标记过程信息类
    主要用于和controller交换json信息
    包含需要提供给网页的信息和返回的标记值
    每一个标记过程产生一个该类的对象
    """
    def __init__(self, name, x, y, rs_rgb_file_name, k, sm_image_dict, label_class_dict):
        """
        初始化函数
        :param name:RS图像名称，区别标记任务
        :param x: 在图像中X位置
        :param y: 在图像中Y位置
        :param rs_rgb_file_name: rgb图像临时文件所在位置
        :param k:聚类参数K
        :param sm_image_dict:聚类中心代表图像文件地址
                key是类别号，value是中心代表图像文件地址
        :param label_class_dict:分类类别
                key是类别编码，value是所代表类别名称
        :return:
        """
        self.__name = name
        self.__x = x
        self.__y = y
        self.__rgb_name = rs_rgb_file_name
        self.__k = k
        self.__image_dict = sm_image_dict
        self.__label_class_dict = label_class_dict

    @property
    def name(self):
        return self.__name

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def rgb_name(self):
        return self.__rgb_name

    @property
    def k(self):
        return self.__k

    @property
    def image_dict(self):
        return self.__image_dict

    @property
    def label_class_dict(self):
        return self.__label_class_dict

def label_process_info_to_json(obj):
    """
    将labelProcessInfo对象转换成json字符串
    :param obj: labelProcessInfo对象
    :return: json字符串
    """
    if isinstance(obj, labelProcessInFo):
        dict = {"name": obj.name,
                "x": obj.x,
                "y": obj.y,
                "rgbName": obj.rgb_name,
                "k": obj.k,
                "imageDict": obj.image_dict,
                "labelClassDict": obj.label_class_dict}
        print(dict)
        return dict
    else:
        return obj

def label_process_info_decode(json_str):
    """
    讲json字符串转为labelProcessInfo对象
    :param json_str: json字符串
    :return: labelProcessInfo对象
    """
    dic = json.loads(json_str)
    print(dic)
    return labelProcessInFo(dic["name"], dic["x"],
                            dic["y"], dic["rgbName"],
                            dic["k"], dic["imageDict"],
                            dic["labelClassDict"]);

def main():
    sm_image_dict = {1: "e:\\1.jpg",
                     2: "e:\\2.jpg",
                     3: "e:\\3.jpg",
                     4: "e:\\4.jpg",
                     5: "e:\\5.jpg"}
    gt = GroundTruth()
    label_class_dict = gt.GTClass
    lp = labelProcessInFo("GF2_shanghai", 1, 2, "e:\\test.jpg", 5, sm_image_dict, label_class_dict)
    lp_json_str = json.dumps(lp, default=label_process_info_to_json)
    print(lp_json_str)
    lp_2 = label_process_info_decode(lp_json_str)
    print(lp_2.name)

if __name__ == "__main__":
    main()

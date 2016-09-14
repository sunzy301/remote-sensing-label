# coding=utf-8
# 提取Oxford5K所有图片的文件名
# 并且存储在一个文件中

import os

def extract_file_name(dir_name, save_name):
    with open(save_name, "w") as f:
        names = os.listdir(dir_name)
        for file_name in names:
            splits = file_name.split(".")
            print(splits[0])
            f.write(splits[0]+"\n")


if __name__ == "__main__":
    extract_file_name("E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\features", "E:\\sun2\\工作\\lab\\遥感数据\\众包标记\\workspace\\oxford5k_names.txt")
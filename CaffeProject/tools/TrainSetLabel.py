# coding=utf-8
# 给每个训练样本分配合适的标记
import os
from CaffeProject.LabelPreprocessing import LoadMetaData
def label(label_file_name="/usr/caffe/data/ILSVRC2012_train_label.txt", root_dir_name="/usr/caffe/data/ILSVRC2012_train"):
    synsets = LoadMetaData.load_meta_data("/root/PycharmProjects/CaffeProject/CaffeProject/data/meta.mat")
    synsets = sorted(synsets, key=lambda synset:synset.label)
    with open(label_file_name, "w") as f:
        for line in synsets:
            label_id = line.label
            wnid = line.wnid
            # print(label, line)
            temp_dir_name = os.path.join(root_dir_name, wnid)
            os.chdir(temp_dir_name)
            print(os.getcwd())
            for image in os.listdir("."):
                f.write(line.wnid+"/"+image+" "+("%d" % label_id)+"\n")


        # jpeg_files = [x for x in os.listdir('.') if os.path.isfile(x)]


if __name__ == "__main__":
    label()
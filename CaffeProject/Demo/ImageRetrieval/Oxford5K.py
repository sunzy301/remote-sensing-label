# coding=utf-8

import os

import numpy

root_path = "/usr/caffe/caffe-master/examples/image_retrieval"
data_path = os.path.join(root_path, "data")
feature_path = os.path.join(root_path, "features")
gt_path = os.path.join(root_path, "groundtruth")

query_name = ["all_souls", "ashmolean", "balliol", "bodleian", "christ_church", "cornmarket",
              "hertford", "keble", "magdalen", "pitt_rivers", "radcliffe_camera"]
query_num = [1, 2, 3, 4, 5]

def image_retrieval():
    image_file_names = []
    for qname in query_name:
        for qnum in query_num:
            query_file_name = qname+"_"+("%d" % qnum)
            with open(os.path.join(gt_path, query_file_name+"_query.txt")) as f:
                words = f.readline().split(" ")
                image_file_names.append(words[0][5:])
    for image_file_name in image_file_names:
        print(image_file_name)
        i_feature = numpy.load(os.path.join(feature_path, image_file_name+".jpg.npy"))
        print(i_feature.shape)


if __name__ == "__main__":
    image_retrieval()
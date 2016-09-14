# coding=utf-8
#
import scipy.io as sio

class synset():
    def __init__(self, id, wnid, synset_name):
        self.id = id
        self.wnid = wnid
        self.synset_name = synset_name

    def __str__(self):
        return ("%d" % self.id)+" "+self.wnid+" "+self.synset_name

def load_meta_data(filename = "E:\\meta.mat"):
    data = sio.loadmat(filename)
    data = data["synsets"]
    num = 0
    # 提取meta.mat中的信息
    synsets = []
    for line in data:
        line = line[0]
        id = line[0][0][0]
        wnid = line[1][0]
        synset_name = line[2][0]
        synsets.append(synset(id, wnid, synset_name))
        num += 1
        if (num == 1000):
            break
    # 按照wnid对于synset进行排序
    sorted_synsets = sorted(synsets, key=lambda synset:synset.wnid)
    num = 0
    # label从0到999
    # 这个方法与caffe中默认的做法是一致的
    for line in sorted_synsets:
        line.label = num
        num += 1
    # for line in sorted_synsets:
    #     print(line.label, lin)
    return synsets

def preprocess_label():
    data = load_meta_data()

if __name__ == "__main__":
    preprocess_label()
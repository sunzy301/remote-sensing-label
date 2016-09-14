# coding=utf-8
import scipy.io as sio
from numpy import *

from CaffeProject.active_learning import AL
from CaffeProject.util.rs_image import RSImage

def RSLabel(dataFileName, labelFileName, numAll, numPerIter, numInitalPerClass, numCand):
    """
    遥感标记数据准备函数，从主界面读入数据
    在该函数中准备数据，并传入AL函数进行主动学习
    :return:
    """

    nband = 103
    # data, label = loadRSMat(data_file_name="/home/dataology/documents/data/PaviaU.mat",
    #                         label_file_name="/home/dataology/documents/data/PaviaU_gt.mat")
    # data, label = loadRSMat()
    rsimage = RSImage(dataFileName, labelFileName)
    # random select trained set, unlabeld pool and validation set
    # print(RSImage.data[0].numBand)
    nonzero_label_loc = nonzero(rsimage.label)
    # data:list[RSPixel]
    data = list(rsimage.data[nonzero_label_loc[0][i]] for i in range(nonzero_label_loc[0].shape[0]))
    # label:ndarray
    label = rsimage.label[nonzero_label_loc[0]]
    label = label-1
    num_sample = len(label)

    trained_list = array([], dtype=int)
    # select trained set from each class
    nclass = len(unique(label))
    num_per_class = numInitalPerClass
    for i in range(nclass):
        range_list = nonzero(label==i)[0]
        range_shuffle_list = arange(len(range_list))
        random.shuffle(range_shuffle_list)
        trained_list = hstack([trained_list, range_list[range_shuffle_list[0:num_per_class]]])

    unselected_list_set = set(range(num_sample))-set(trained_list.tolist())
    unselected_list = array(list(unselected_list_set))
    unselected_shuffle_list = arange(unselected_list.shape[0])
    random.shuffle(unselected_shuffle_list)

    ncand = numCand
    unlabeled_pool_list = unselected_list[unselected_shuffle_list[0:ncand]]
    val_set_list = unselected_list[unselected_shuffle_list[ncand:]]


    # the last column is label
    labeled_set = list(data[trained_list[i]] for i in range(trained_list.shape[0]))
    unlabeled_pool = list(data[unlabeled_pool_list[i]] for i in range(unlabeled_pool_list.shape[0]))
    val_set = list(data[val_set_list[i]] for i in range(val_set_list.shape[0]))

    print("num val set", len(labeled_set))
    print("num val set", len(unlabeled_pool))
    print("num val set", len(val_set))
    # print(list(iter))

    AL.al(labeled_set, unlabeled_pool, val_set, nband, iterVector=range(1, numAll, numPerIter))
    print("AL done")



def RSLabelTest():
    """
    遥感数据标记测试函数
    :return:
    """
    nband = 103
    # data, label = loadRSMat(data_file_name="/home/dataology/documents/data/PaviaU.mat",
    #                         label_file_name="/home/dataology/documents/data/PaviaU_gt.mat")
    # data, label = loadRSMat()
    rsimage = RSImage("E:\\PaviaU.mat", "E:\\PaviaU_gt.mat")
    # random select trained set, unlabeld pool and validation set
    nonzero_label_loc = nonzero(rsimage.label)
    # data:list[RSPixel]
    data = list(rsimage.data[nonzero_label_loc[0][i]] for i in range(nonzero_label_loc[0].shape[0]))
    # label:ndarray
    label = rsimage.label[nonzero_label_loc[0]]
    label = label-1
    num_sample = len(label)

    trained_list = array([], dtype = int)
    # select trained set from each class
    nclass = len(unique(label))
    num_per_class = 10
    for i in range(nclass):
        range_list = nonzero(label==i)[0]
        range_shuffle_list = arange(len(range_list))
        random.shuffle(range_shuffle_list)
        trained_list = hstack([trained_list, range_list[range_shuffle_list[0:num_per_class]]])

    unselected_list_set = set(range(num_sample))-set(trained_list.tolist())
    unselected_list = array(list(unselected_list_set))
    unselected_shuffle_list = arange(unselected_list.shape[0])
    random.shuffle(unselected_shuffle_list)

    ncand = 10000
    unlabeled_pool_list = unselected_list[unselected_shuffle_list[0:ncand]]
    val_set_list = unselected_list[unselected_shuffle_list[ncand:]]


    # the last column is label
    labeled_set = list(data[trained_list[i]] for i in range(trained_list.shape[0]))
    unlabeled_pool = list(data[unlabeled_pool_list[i]] for i in range(unlabeled_pool_list.shape[0]))
    val_set = list(data[val_set_list[i]] for i in range(val_set_list.shape[0]))

    print(len(labeled_set))
    print(len(unlabeled_pool))
    print(len(val_set))

    AL.al(labeled_set, unlabeled_pool, val_set, nband, iterVector=range(0, 10, 10))

    # baseline classification

    # trained_set = labeled_set
    # trained_set.extend(unlabeled_pool)
    # AL.baseline_assesment(trained_set, val_set)





def loadRSMat(data_file_name="E:\\PaviaU.mat", label_file_name="E:\\PaviaU_gt.mat"):
    """
    从mat文件中读取遥感数据，并进行正则化
    :param data_file_name: 特征数据文件位置
    :param label_file_name: 标记数据文件位置
    :return: 返回正则化好的特征数据以及标记数据，都是ndarray格式
    """

    nx = 610
    ny = 340
    nband = 103
    # load mat file
    data = sio.loadmat(data_file_name)
    label = sio.loadmat(label_file_name)
    # reshape
    data = data["paviaU"].reshape(nx*ny, nband)
    label = label["paviaU_gt"].reshape(nx*ny, 1)

    print(data.shape)
    print(label.shape)
    # normalize
    maxx = tile(data.max(0), (nx*ny, 1))
    minn = tile(data.min(0), (nx*ny, 1))
    # x,y location on the RS image
    x = tile(arange(nx), (ny, 1)).T
    y = tile(arange(ny), (nx, 1))

    # +0.0 for both py 2.7.x and 3.x
    data = (data-minn)/(maxx-minn+0.0)

    return data, label

if __name__ == "__main__":
    RSLabel()

# coding=utf-8
# 分类器
# 分类算法库使用scikit
from sklearn import svm

import numpy as np
from numpy import *
from CaffeProject.util import basic_func
from sklearn.grid_search import GridSearchCV

def train(train_set, **options):
    """
    训练分类器.
    :param train_set: 训练数据集
    :param options: 参数选项
    :return: 返回一个训练好的model
    """
    if not ("model_type" in options):
        model_type = "SVM"
    else:
        model_type = options["model_type"]
    if not ("para" in options):
        parameter = ""
    else:
        parameter = options["para"]

    classifiers = {"SVM": SVM_train}

    classifier_model = classifiers.get(model_type)(train_set, parameter)



    return classifier_model

def SVM_train(train_set, parameter):

    clf = svm.SVC()

    clf.__init__(C=parameter["C"], gamma=parameter["gamma"])
    # clf.__init__(C=31, gamma=10)
    train_set_feature_array, train_set_label_array = basic_func.list2ndarray(train_set)
    clf.fit(train_set_feature_array, train_set_label_array)

    return clf

def predict(test_set, model, **options):
    """
    测试数据集.
    :param test_set: 测试数据集
    :param model: 训练好的模型
    :param options: 参数选项
    :return: 返回对于每个样本的预测类别
    """
    if not ("model_type" in options):
        model_type = "SVM"
    else:
        model_type = options["model_type"]
    if not ("para" in options):
        parameter = ""
    else:
        parameter = options["para"]

    classifiers = {"SVM": SVM_predict}
    predict_label = classifiers.get(model_type)(test_set, model, parameter)
    return predict_label


def SVM_predict(test_set, model, para):
    predict_feature_array, predict_label = basic_func.list2ndarray(test_set)
    predict_label = model.predict(predict_feature_array)
    return predict_label


def predict_with_distance(test_set, model, **options):
    """
    测试数据集并且返回分类依据.
    :param test_set: 测试数据集
    :param model: 训练好的模型
    :param options: 参数选项
    :return: 返回对于每个样本的预测类别和预测根据（对于SVM是距离，对于LR是概率值）
    """
    """
    测试数据集.
    :param test_set: 测试数据集
    :param model: 训练好的模型
    :param options: 参数选项
    :return: 返回对于每个样本的预测类别
    """
    if not ("model_type" in options):
        model_type = "SVM"
    else:
        model_type = options["model_type"]
    if not ("para" in options):
        parameter = ""
    else:
        parameter = options["para"]

    classifiers = {"SVM": SVM_predict_with_distance}
    predict_label, predict_distance = classifiers.get(model_type)(test_set, model, parameter)
    return predict_label, predict_distance

def SVM_predict_with_distance(test_set, model, para):
    predict_feature_array, predict_label = basic_func.list2ndarray(test_set)
    predict_label = model.predict(predict_feature_array)
    predict_distance = model.decision_function(predict_feature_array)
    return predict_label, predict_distance

def assesment(predict_label, ground_truth):
    """
    评估分类结果
    :param predict_label: 分类器预测的类别
    :param ground_truth: 样本实际的类别
    :return: 返回准确率
    """
    n = 0
    for i in range(len(predict_label)):
        if predict_label[i] == ground_truth[i]:
            n += 1
    return n

def gird_search(labeled_set, **options):
    """
    交叉检索找寻最佳参数
    :param labeled_set: 存在标记的样本数据集
    :param options: 参数选项
    :return: 最佳参数组成的dict
    """
    if not ("model_type" in options):
        model_type = "SVM"
    else:
        model_type = options["model_type"]
    if not ("para" in options):
        parameter = ""
    else:
        parameter = options["para"]

    grid_search_models = {"SVM": SVM_RBF_grid_search}
    best_para = grid_search_models.get(model_type)(labeled_set)
    return best_para


def SVM_RBF_grid_search(labeled_set):
    print("grid search")
    clf = svm.SVC()
    Cs = np.logspace(0, 2, 5)
    sigmas = np.logspace(-2, 1, 5)
    parameters = {"gamma": sigmas,
              "C": Cs}
    grid_search = GridSearchCV(estimator=clf, param_grid=parameters, n_jobs=1)

    labeled_set_feature_array, temp_label = basic_func.list2ndarray(labeled_set)
    temp_label = asarray(temp_label).reshape(-1)
    print(labeled_set_feature_array.shape)
    print(temp_label.shape)

    grid_search.fit(labeled_set_feature_array, temp_label)


    print(grid_search.best_estimator_.C, grid_search.best_estimator_.gamma)
    return {"C": grid_search.best_estimator_.C, "gamma": grid_search.best_estimator_.gamma}
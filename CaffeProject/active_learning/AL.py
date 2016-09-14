# coding=utf-8
# 主动学习主过程
from numpy import *

from CaffeProject.active_learning import divertsity_strategies as DS, uncertainty_strategies as US
from CaffeProject.crowd_sourcing import label
from CaffeProject.machine_learning import Classifier
from CaffeProject.util import basic_func


def al(labeled_set, unlabeled_set, val_set, nband, **options  ):
    """
    用于有测试标记数据的情况
    主动学习主函数
    所有数据集格式都是list[RSPixel]
    :param labeled_set: 有标记的初始训练数据集
    :param unlabeled_set: 未标记的样本池
    :param val_set: 验证数据集
    :param options: 参数选项
        uncertainty
        diversity
        iterVector
        model
        classifierPara
    :return:
    """
    # parameters check
    if not ("model_type" in options):
        model = "SVM"
    else:
        model = options["model_type"]
    if not ("uncertainty" in options):
        uncertainty = "MS"
    else:
        uncertainty = options["uncertainty"]
    if not ("diversity" in options):
        diversity = "NONE"
    else:
        diversity = options["diversity"]
    if not ("iterVector" in options):
        iterVector = range(1, 10)
    else:
        iterVector = options["iterVector"]
    if not ("classifierPara" in options):
        classifierPara = ""
    else:
        classifierPara = options["classifierPara"]

    if not (model in ["SVM"]):
        raise(Exception("Unsupported model"))
    if not (uncertainty in ["MS", "MCLU", "RAND"]):
        raise(Exception("Unsupported uncertainty strategy"))
    if not (diversity in ["ECBD", "ABD", "CEAL", "NONE"]):
        raise(Exception("Unsupported diversity strategy"))

    acc_curve = zeros((len(iterVector), 1))
    diff_vect = diff(iterVector)
    print(list(iterVector))
    for i in range(len(iterVector)):
        print("")
        print("")
        print("-----------", i, "th iteration ---------------")
        # grid search
        if i % 10 == 0:
            best_para = Classifier.gird_search(labeled_set)

        # train the classifier
        classifier_model = Classifier.train(labeled_set, para=best_para)
        # print(classifier_model)
        # predictions on the val st
        predict_val_labels = Classifier.predict(val_set, classifier_model)

        # assesment
        val_set_label = basic_func.listSelectLabel(val_set)
        acc_curve[i] = Classifier.assesment(predict_val_labels, val_set_label)
        print("accuarcy is :", acc_curve[i]/(len(val_set)+0.0)*100, "%")
        if i == len(iterVector)-1:
            break

        # if i == len(iterVector):
        #     break

        # predictions on the unlabeled pool
        predict_pool_labels, predict_pool_distance = Classifier.predict_with_distance(unlabeled_set, classifier_model)

        # rank the predicitons
        uncertainty_strategies = {"RAND": US.rand, "MS": US.ms, "MCLU": US.mclu}
        diversity_strategies = {"NONE": DS.none, "ABD": DS.abd, "ECBD": DS.ecbd, "CEAL": DS.ceal}
        sorted_distance, sorted_index = uncertainty_strategies.get(uncertainty)(predict_pool_distance)
        index = diversity_strategies.get(diversity)(sorted_distance, sorted_index)

        # select samples from unlabeled pool and manual labelling
        select_list = index[:diff_vect[i]]
        select_samples = list(unlabeled_set[select_list[i]] for i in range(len(select_list)))
        # 标记工作在Label中完成，直接标在select_samples中RSPixel的Label中
        label.label_auto(select_samples)
        # print(select_label.shape)
        # add labeled samples to labeled set and remove them from unlabeled pool
        # select_samples = hstack([unlabeled_set[select_list, :-1], select_label])
        # labeled_set = vstack([labeled_set, select_samples])
        labeled_set.extend(select_samples)

        # mask = ones(unlabeled_set.shape[0], dtype=bool)
        # mask[select_list] = False
        # unlabeled_set = unlabeled_set[mask, ...]
        unlabeled_set = [unlabeled_set[i] for i in range(len(unlabeled_set)) if i not in select_list]
        print(len(unlabeled_set), len(labeled_set))

def baseline_assesment(labeled_set, val_set):
    # grid search
    best_para = Classifier.gird_search(labeled_set)
    classifier_model = Classifier.train(labeled_set, para=best_para)

    # predictions on the val st
    predict_val_labels = Classifier.predict(val_set, classifier_model)

    # assesment
    acc_curve = Classifier.assesment(predict_val_labels, val_set[:, -1])
    print(acc_curve/(val_set.shape[0]+0.0)*100)

def al_one_step(labeled_set, unlabeled_set, nband, batch_size, **options):
    """
    主动学习单步
    根据标记数据集训练一个模型
    然后从未标记数据集中选择需要人工标记的样本
    :param labeled_set:已有标记数据集，作为训练集
    :param unlabeled_set: 未标记数据池
    :param batch_size: 需要挑选出的未标记样本数量
    :param options:参数选项
    :return:需要人工标记样本列表
            List[Int]，其中是每个RSPixel的ID
    """
    # 参数检查
    # parameters check
    if not ("model_type" in options):
        model = "SVM"
    else:
        model = options["model_type"]
    if not ("uncertainty" in options):
        uncertainty = "MS"
    else:
        uncertainty = options["uncertainty"]
    if not ("diversity" in options):
        diversity = "NONE"
    else:
        diversity = options["diversity"]


    if not (model in ["SVM"]):
        raise(Exception("Unsupported model"))
    if not (uncertainty in ["MS", "MCLU", "RAND"]):
        raise(Exception("Unsupported uncertainty strategy"))
    if not (diversity in ["ECBD", "ABD", "CEAL", "NONE"]):
        raise(Exception("Unsupported diversity strategy"))

    # 自动选择最佳参数
    best_para = Classifier.gird_search(labeled_set)

    # train the classifier
    classifier_model = Classifier.train(labeled_set, para=best_para)

    # predictions on the unlabeled pool
    predict_pool_labels, predict_pool_distance = Classifier.predict_with_distance(unlabeled_set, classifier_model)

    # rank the predicitons
    uncertainty_strategies = {"RAND": US.rand, "MS": US.ms, "MCLU": US.mclu}
    diversity_strategies = {"NONE": DS.none, "ABD": DS.abd, "ECBD": DS.ecbd, "CEAL": DS.ceal}
    sorted_distance, sorted_index = uncertainty_strategies.get(uncertainty)(predict_pool_distance)
    index = diversity_strategies.get(diversity)(sorted_distance, sorted_index)

    # select samples from unlabeled pool and manual labelling
    select_list = index[:batch_size]
    samples_index_list = list(unlabeled_set[select_list[i]].id for i in range(len(select_list)))
    return samples_index_list





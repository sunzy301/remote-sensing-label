# coding=utf-8
# 聚类算法
from sklearn import cluster
def clustering(feature_sets, **options):
    if "k" not in options:
        options["k"] = 5
    k_means = cluster.KMeans(n_clusters=options["k"])
    k_means.fit(feature_sets)
    return k_means.labels_, k_means.cluster_centers_

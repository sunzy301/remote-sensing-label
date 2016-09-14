# kmeans
from sklearn import cluster, datasets
iris = datasets.load_iris()
print(iris.data.shape)
k_means = cluster.KMeans(n_clusters=3)
k_means.fit(iris.data)
print(k_means)
print(k_means.labels_)
print(k_means.cluster_centers_)
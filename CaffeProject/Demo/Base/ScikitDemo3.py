# coding=utf-8
# demo for pca
from sklearn import datasets, decomposition
import numpy
iris = datasets.load_iris()
print(iris.data.shape)

pca = decomposition.PCA(n_components=2)
new_data = pca.fit_transform(iris.data)
d = numpy.array([1,2,3,4])
c = pca.transform(d)
print(c)
print(new_data.shape)
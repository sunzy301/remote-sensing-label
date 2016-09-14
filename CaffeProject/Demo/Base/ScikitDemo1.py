# svm
from sklearn import datasets
from sklearn import svm
from sklearn.grid_search import GridSearchCV
import numpy as np
iris = datasets.load_iris()
digits = datasets.load_digits()
print(digits.data.shape)
print("grid search")
sigmas = np.logspace(-2, 1, 5)
Cs = np.logspace(0, 2, 5)

parameters = {"gamma": sigmas,
              "C": Cs
              }

clf = svm.SVC()
print(clf)
grid_search1 = GridSearchCV(estimator=clf, param_grid=parameters, n_jobs=1)
print(digits.data[:-1].shape)
print(digits.target[:-1].shape)

grid_search1.fit(digits.data[:-1], digits.target[:-1])
print(grid_search1.best_estimator_.C)
print(grid_search1.best_estimator_.gamma)

# grid_search1 = GridSearchCV(estimator=clf, param_grid=dict(gamma=sigmas), n_jobs=1)
# grid_search1.fit(digits.data[:-1], digits.target[:-1])
# print(grid_search1.best_estimator_.gamma)

clf.fit(digits.data[:-1], digits.target[:-1])
print(clf.predict(digits.data[-1]))
# print(clf.decision_function(digits.data[-1]))

clf.__init__(C=grid_search1.best_estimator_.C, gamma=grid_search1.best_estimator_.gamma)
clf.fit(digits.data[:-1], digits.target[:-1])



# load matlab .mat file
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np

#matlab文件名
matfn = "e:\\PaviaU.mat"
data = sio.loadmat(matfn)
print(data["paviaU"].shape)
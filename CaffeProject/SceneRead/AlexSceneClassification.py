
from matplotlib import pyplot as plt
import numpy as np

import time
import caffe
# using alexnet
caffe_root = "/usr/caffe/caffe-master/"
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

model_file = "/usr/caffe/caffe-master/examples/scene_read/alexnet_places2/alexnet_places2/deploy.prototxt"
pretrained = "/usr/caffe/caffe-master/examples/scene_read/alexnet_places2/alexnet_places2/alexnet_places2.caffemodel"

caffe.set_device(0)

caffe.set_mode_gpu()
net = caffe.Net(model_file, pretrained, caffe.TEST)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

net.blobs['data'].reshape(10, 3, 227, 227)
print(type(net.blobs["data"].data))
net.blobs['data'].data[0, ...] = transformer.preprocess('data', caffe.io.load_image("/home/dataology/workspace/caffe/scene/kitchen1.jpeg"))
net.blobs['data'].data[1:9, ...] = transformer.preprocess('data', caffe.io.load_image("/home/dataology/workspace/caffe/scene/dfmz1.jpg"))

print(net.blobs["data"].data.shape)
start = time.time()
out = net.forward()
end = time.time()

print(end-start)
n = 2
# for i in range(50):
#  print("Predicted class is #{}.".format(out['prob'][i].argmax()))

plt.imshow(transformer.deprocess('data', net.blobs['data'].data[0]))
# plt.show()


# load labels
imagenet_labels_filename = "/usr/caffe/caffe-master/examples/scene_read/alexnet_places2/alexnet_places2/categories.txt"
try:
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
except:
    # !../data/ilsvrc12/get_ilsvrc_aux.sh
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

# sort top k predictions from softmax output

top_k = net.blobs['prob'].data[1].flatten().argsort()[-1:-6:-1]
print labels[top_k]





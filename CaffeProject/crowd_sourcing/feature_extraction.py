# coding=utf-8
# 图像特征提取
from CaffeProject.util.image_set import *
from CaffeProject.util.socialmedia_image import *
from numpy import *
import numpy
# import caffe
def extract(image_set, **options):
    """
    对于一个图片数据集中所有图片输出一个特征
    :param image_set: 图片数据集
    :param options: 可选控制项
    :return:
    """
    for (k, v) in image_set.image_set.items():
        # v.feature = cnn_image_extraction(v.imageArray)
        v.feature = random_image_extraction(v.imageArray)

def cnn_image_extraction(image_set):
    caffe_root = "/usr/caffe/caffe-master/"

    model_file = "/usr/caffe/caffe-master/models/bvlc_reference_caffenet/deploy.prototxt"
    pretrained = "/usr/caffe/caffe-master/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel"

    caffe.set_device(0)
    caffe.set_mode_gpu()
    net = caffe.Net(model_file, pretrained, caffe.TEST)

    # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2, 1, 0))  # the reference model has channels in BGR order instead of RGB

    net.blobs['data'].reshape(len(image_set.iset), 3, 227, 227)
    for (k, v) in image_set.iset.items():
        net.blobs['data'].data[k, ...] = transformer.preprocess('data', caffe.io.load_image(v.filename))

    out = net.forward()
    print(net.blobs["fc7"].data.shape)

    for (k, v) in image_set.iset.items():
        v.feature = net.blobs["fc7"].data[k, ...]





def random_image_extraction(image):
    return random.rand(ImageSet.featureNum, 1)

if __name__ == "__main__":
    IS = ImageSet()
    image = SMImage(0, "/usr/caffe/caffe-master/examples/images/cat.jpg")
    IS.add(0, image)
    IS.add(1, image)
    # IS.load_all()
    cnn_image_extraction(IS)
    # print(IS.iset[0].feature.shape)

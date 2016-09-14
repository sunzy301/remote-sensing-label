from CaffeProject.Util.image_set import *
from CaffeProject.Util.socialmedia_image import *
from numpy import *
import numpy
import caffe

class spoc_feature_info(object):
    def __init__(self, conv_name, conv_num):
        self.conv_name = conv_name
        self.conv_num = conv_num
        # self.height = height
        # self.width = width

def cnn_image_extraction_from_dir(dir_name, feature_name):
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

    block_num = 64
    net.blobs['data'].reshape(block_num, 3, 227, 227)
    images = os.listdir(dir_name)
    now_num = 0
    total_num = 0
    image_names = []
    conv_spoc_feature_info = []
    for image_name in images:
        print(total_num)

        image_names.append(image_name)
        net.blobs['data'].data[now_num, ...] = transformer.preprocess('data', caffe.io.load_image(os.path.join(dir_name, image_name)))
        if now_num == block_num-1:
            out = net.forward()
            print(net.blobs)
            print(net.blobs["fc6"].data[1, :].shape)
            if total_num == block_num-1:
                # for the first time, inital the spoc conv feature info
                # conv_feature4 = spoc_feature_info("conv4", net.blobs["conv4"].data.shape[1], net.blobs["conv4"].data.shape[2],net.blobs["conv4"].data.shape[3])
                # conv_feature5 = spoc_feature_info("conv5", net.blobs["conv5"].data.shape[1], net.blobs["conv5"].data.shape[2],net.blobs["conv5"].data.shape[3])
                # conv_spoc_feature_info.append(conv_feature4)
                # conv_spoc_feature_info.append(conv_feature5)
                drop_feature_info = spoc_feature_info("fc6", net.blobs["fc6"].data.shape[1])
                conv_spoc_feature_info.append(drop_feature_info)
            num_conv_feature_total = 0
            for i in range(len(conv_spoc_feature_info)):
                num_conv_feature_total +=conv_spoc_feature_info[i].conv_num
            print(num_conv_feature_total)
            conv_features = [0]*num_conv_feature_total
            for i in range(now_num+1):
                ii = 0
                for k in range(len(conv_spoc_feature_info)):
                    conv_features[ii] = net.blobs[conv_spoc_feature_info[k].conv_name].data[i, :]
                    print(net.blobs[conv_spoc_feature_info[k].conv_name].data[i, :])
                    ii += 1
                str = image_names[i]+".npy"
                print(str)
                conv_features_array = array(conv_features)
                numpy.save(os.path.join(feature_name, str), conv_features_array)
            now_num = 0
            image_names = []
            # break
        else:
            now_num += 1
        total_num += 1
    print(now_num)
    for i in range(now_num):
        ii = 0
        for k in range(len(conv_spoc_feature_info)):
                conv_features[ii] = net.blobs[conv_spoc_feature_info[k].conv_name].data[i, :]
                ii += 1
        str = image_names[i]+".npy"
        print(str)
        conv_features_array = array(conv_features)
        numpy.save(os.path.join(feature_name, str), conv_features_array)

    print(total_num)



if __name__ == "__main__":
    # cnn_image_extraction_from_dir("/usr/caffe/caffe-master/examples/image_retrieval/data/", "/usr/caffe/caffe-master/examples/image_retrieval/features")
    a = numpy.load("/usr/caffe/caffe-master/examples/image_retrieval/features/worcester_000198.jpg.npy")
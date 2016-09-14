
from matplotlib import pyplot as plt
import numpy as np

import time
import caffe
import os
import shutil
# using vgg
"""
caffe_root = "/usr/caffe/caffe-master/"
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

model_file = "/usr/caffe/caffe-master/examples/scene_read/vgg16_places2/vgg16_places2/deploy.prototxt"
pretrained = "/usr/caffe/caffe-master/examples/scene_read/vgg16_places2/vgg16_places2/vgg16_places2.caffemodel"

caffe.set_device(0)

caffe.set_mode_gpu()
net = caffe.Net(model_file, pretrained, caffe.TEST)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

# load images
# 10 is the number of batch
# the number is decided by the memory of GPU
net.blobs['data'].reshape(10, 3, 224, 224)
print(type(net.blobs["data"].data))
#net.blobs['data'].data[0, ...] = transformer.preprocess('data', caffe.io.load_image("/home/dataology/workspace/caffe/scene/kitchen1.jpeg"))
#net.blobs['data'].data[1, ...] = transformer.preprocess('data', caffe.io.load_image("/home/dataology/workspace/caffe/scene/dfmz1.jpg"))
# EDIT HERE
for i in range(10):
    net.blobs['data'].data[i, ...] = transformer.preprocess('data', caffe.io.load_image("/home/dataology/workspace/caffe/scene/1/"+str(i+1)+".jpg"))


# one batch of samples prediction
print(net.blobs["data"].data.shape)
start = time.time()
out = net.forward()
end = time.time()

# the time of the prediction
# about 0.5s for vgg16 and 0.08s for alexnet
print(end-start)
n = 2
# for i in range(50):
#  print("Predicted class is #{}.".format(out['prob'][i].argmax()))

# plt.imshow(transformer.deprocess('data', net.blobs['data'].data[0]))
# plt.show()


# load labels
imagenet_labels_filename = "/usr/caffe/caffe-master/examples/scene_read/vgg16_places2/vgg16_places2/categories.txt"
try:
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
except:
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

# sort top k predictions from softmax output

#top_k = net.blobs['prob'].data[1].flatten().argsort()[-1:-6:-1]
#print labels[top_k]
# EDIT HERE
# the classiciation output of the i-st image
for i in range(10):
    top_k = net.blobs['prob'].data[i].flatten().argsort()[-1:-6:-1]
    print labels[top_k]
"""

#The following codes are modified by Qin Yiqing
def proceed_10_images(target_directory,start_image_no,result_file):

    #net.blobs['data'].data[0, ...] = transformer.preprocess('data', caffe.io.load_image("/home/dataology/workspace/caffe/scene/kitchen1.jpeg"))
    #net.blobs['data'].data[1, ...] = transformer.preprocess('data', caffe.io.load_image("/home/dataology/workspace/caffe/scene/dfmz1.jpg"))
    # EDIT HERE
    bad_image_no=[0,1,2,3,4,5,6,7,8,9]
    for i in range(10):
        try:
            net.blobs['data'].data[i, ...] = transformer.preprocess('data', caffe.io.load_image(target_directory+str(start_image_no+i)+".jpg"))
            bad_image_no.remove(i)
        except:
            pass


    # one batch of samples prediction
    print(net.blobs["data"].data.shape)
    start = time.time()
    out = net.forward()
    end = time.time()

    # the time of the prediction
    # about 0.5s for vgg16 and 0.08s for alexnet
    print(end-start)
    n = 2
    # for i in range(50):
    #  print("Predicted class is #{}.".format(out['prob'][i].argmax()))

    # plt.imshow(transformer.deprocess('data', net.blobs['data'].data[0]))
    # plt.show()


    # load labels
    imagenet_labels_filename = "/usr/caffe/caffe-master/examples/scene_read/vgg16_places2/vgg16_places2/categories.txt"
    try:
        labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
    except:
        labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

    # sort top k predictions from softmax output

    #top_k = net.blobs['prob'].data[1].flatten().argsort()[-1:-6:-1]
    #print labels[top_k]
    # EDIT HERE
    # the classiciation output of the i-st image
    for i in range(10):
        if i in bad_image_no:
            print("bad image")
            result_file.write("bad image\n")
        else:
            top_k = net.blobs['prob'].data[i].flatten().argsort()[-1:-6:-1]
            print labels[top_k]
            result_file.write(str(labels[top_k])+"\n")
        result_file.flush()

def get_images_number(target_directory):
    image_number=0
    while True:
        if os.path.exists(target_directory+str(image_number+1)+".jpg"):
            image_number+=1
        else:
            return image_number

def proceed_a_word(target_directory):
    if os.path.exists((target_directory+"VGG_output.txt")):
        return 1
    result_file=open(target_directory+"VGG_output(unfinished).txt",'w')
    start_image_no = 1
    finish_image_no=get_images_number(target_directory)
    while start_image_no <= finish_image_no:
        proceed_10_images(target_directory,start_image_no,result_file)
        start_image_no += 10
    os.rename(target_directory+"VGG_output(unfinished).txt",target_directory+"VGG_output.txt")
    return 0

#start
#initialize
caffe_root = "/usr/caffe/caffe-master/"
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

model_file = "/usr/caffe/caffe-master/examples/scene_read/vgg16_places2/vgg16_places2/deploy.prototxt"
pretrained = "/usr/caffe/caffe-master/examples/scene_read/vgg16_places2/vgg16_places2/vgg16_places2.caffemodel"

caffe.set_device(0)

caffe.set_mode_gpu()
net = caffe.Net(model_file, pretrained, caffe.TEST)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

# load images
# 10 is the number of batch
# the number is decided by the memory of GPU
net.blobs['data'].reshape(10, 3, 224, 224)

#initialize finished

base_directory="/usr/caffe/images of the buildings/"
proceeded_words=1
for sub_directory in os.listdir(base_directory):
    if sub_directory!="words.txt":
        print("current processing word:"+str(sub_directory))
        target_directory=base_directory+sub_directory+"/"
        if proceed_a_word(target_directory)==0:
            proceeded_words+=1
        if proceeded_words%100==0:
            print("The process is sleeping and will be resumed after 1000 seconds.")
            time.sleep(1000)
    else:
        continue
print ("Process finished.")

"""
destination_base_directory="/home/dataology/workspace/caffe/scene/VGG_result/"
for sub_directory in os.listdir(base_directory):
    if sub_directory!="words.txt":
        os.mkdir(destination_base_directory+sub_directory)
        destination_target_directory=destination_base_directory+sub_directory+"/"
        target_directory=base_directory+sub_directory+"/"
        target_file=target_directory+"VGG_output.txt"
        shutil.copy(target_file,destination_target_directory+"VGG_output.txt")
"""






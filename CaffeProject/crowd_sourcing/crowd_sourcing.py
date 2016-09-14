# coding=utf-8
# crowd-soiurcing labelling
import sys
from PyQt4 import QtGui, QtCore
from PIL import Image
from CaffeProject.GUI import LabelWindow
def CrowdSourcingLabel(RSImage, image_set, cluster_id, coordinate, sample, **options):
    # get the RGB image of RGImage
    RSRGBImage = []
    cluster_image = []
    for i in range(cluster_id):
        tempFileName = image_set._iset[cluster_id[i]].filename
    app = QtGui.QApplication(sys.argv)
    widget = LabelWindow()
    widget.show()
    app.exec_()
    # delete remote sensing RGB image
    # delete cluster center images






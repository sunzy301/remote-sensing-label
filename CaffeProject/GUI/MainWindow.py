# coding=utf-8
# main window

import sys
import os
from PyQt4 import QtGui, QtCore
from CaffeProject.util.rs_image import RSImage
from CaffeProject.active_learning import remote_sensingLabel
from CaffeProject.util import basic_func
from CaffeProject.util.parameter import Para
from numpy import *
from scipy.misc import imsave


class LabelWindow(QtGui.QWidget):
    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Main Window')
        # overall layout
        widgetLayout = QtGui.QHBoxLayout()

        # left layout
        leftLayout = QtGui.QVBoxLayout()
        self.openDataButton = QtGui.QPushButton(self)
        self.openDataButton.setObjectName("openDataButton")
        self.openDataButton.setText("Load Image File")
        self.openDataButton.clicked.connect(self.openImage)
        self.openLabelButton = QtGui.QPushButton(self)
        self.openLabelButton.setObjectName("openLabeklButton")
        self.openLabelButton.setText("Load Label File")
        self.openLabelButton.clicked.connect(self.openLabel)
        # rgb layout
        rgbLayout = QtGui.QGridLayout()
        rgbLayout.setSpacing(10)
        # console1 for file
        self.console1 = QtGui.QLabel()
        # console2 for rgb
        self.console2 = QtGui.QLabel()
        # console3 for al
        self.console3 = QtGui.QLabel()
        redButton = QtGui.QLabel("RED")
        greenButton = QtGui.QLabel("GREEN")
        blueButton = QtGui.QLabel("BLUE")
        rgbLayout.addWidget(redButton, 0, 0)
        rgbLayout.addWidget(greenButton, 0, 1)
        rgbLayout.addWidget(blueButton, 0, 2)
        self.redLoad = QtGui.QLineEdit()
        self.greenLoad = QtGui.QLineEdit()
        self.blueLoad = QtGui.QLineEdit()
        rgbLayout.addWidget(self.redLoad, 1, 0)
        rgbLayout.addWidget(self.greenLoad, 1, 1)
        rgbLayout.addWidget(self.blueLoad, 1, 2)
        self.showButton = QtGui.QPushButton()
        self.showButton.setText("SHOW RS IMAGE")
        self.showButton.clicked.connect(self.RGBLoad)
        rgbLayout.addWidget(self.showButton, 2, 0)
        #
        leftLayout.addWidget(self.openDataButton)
        leftLayout.addWidget(self.openLabelButton)
        leftLayout.addLayout(rgbLayout)
        leftLayout.addWidget(self.console1)
        leftLayout.addWidget(self.console2)
        leftLayout.addWidget(self.console3)

        # right layout
        rightLayout = QtGui.QGridLayout()
        rightLayout.setSpacing(3)
        numAButton = QtGui.QLabel("Num All")
        numPButton = QtGui.QLabel("Num Round")
        numIButton = QtGui.QLabel("Num Class")
        numCButton = QtGui.QLabel("Num Cand")
        self.numALoad = QtGui.QLineEdit()
        self.numPLoad = QtGui.QLineEdit()
        self.numILoad = QtGui.QLineEdit()
        self.numCLoad = QtGui.QLineEdit()
        rightLayout.addWidget(numAButton, 0, 0)
        rightLayout.addWidget(numPButton, 1, 0)
        rightLayout.addWidget(numIButton, 2, 0)
        rightLayout.addWidget(numCButton, 3, 0)
        rightLayout.addWidget(self.numALoad, 0, 1)
        rightLayout.addWidget(self.numPLoad, 1, 1)
        rightLayout.addWidget(self.numILoad, 2, 1)
        rightLayout.addWidget(self.numCLoad, 3, 1)
        self.alButton = QtGui.QPushButton()
        self.alButton.setText("Do AL Process")
        self.alButton.clicked.connect(self.ALLoad)
        self.consoleOut = QtGui.QLabel()
        rightLayout.addWidget(self.alButton, 4, 0)


        # middle
        self.middleRSButton = QtGui.QToolButton()
        # remote sensing RGB image
        self.middleRSButton.setIcon(QtGui.QIcon())
        self.middleRSButton.setIconSize(QtCore.QSize(300, 500))
        widgetLayout.addLayout(leftLayout)
        widgetLayout.addWidget(self.middleRSButton)
        widgetLayout.addLayout(rightLayout)
        self.setLayout(widgetLayout)

    def openImage(self):
        # read rs image file name
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Select Image File", "E:\\")
        print(fileName)
        self.RS_image_file_name = fileName
        self.console1.setText(fileName)

    def openLabel(self):
        # read rs label file name
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Select Label File", "E:\\")
        print(fileName)
        self.RS_label_file_name = fileName
        self.console1.setText(fileName)

    def RGBLoad(self):
        # for py2.7
        # r = int(unicode(self.redLoad.text(), "ASCII", "ignore"))
        # g = int(unicode(self.greenLoad.text(), "ASCII", "ignore"))
        # b = int(unicode(self.blueLoad.text(), "ASCII", "ignore"))

        # for py3.4
        r = int(self.redLoad.text())
        g = int(self.greenLoad.text())
        b = int(self.blueLoad.text())
        print(r, g, b)
        tempstr = "R:%d G:%d B:%d" % (r, g, b)
        self.console2.setText(tempstr)

        rsimage = RSImage(self.RS_image_file_name, self.RS_label_file_name)
        data = basic_func.list2ndarray(rsimage.data)[0]
        data = reshape(data, [rsimage.numX, rsimage.numY, rsimage.nband])
        print(data.shape)
        rgbimage = data[:, :, ix_([r, g, b])]
        rgbimage = reshape(rgbimage, [rsimage.numX, rsimage.numY, 3])
        # rimage = data[:, :, r]
        # gimage = data[:, :, g]
        # bimage = data[:, :, b]
        # rgbimage = hstack(rimage, gimage, bimage)
        print(rgbimage.shape)
        imagesavename = os.path.join(Para.root, "tmp\\test.jpg")
        imsave(imagesavename, rgbimage)
        self.middleRSButton.setIcon(QtGui.QIcon(imagesavename))

    def ALLoad(self):
        # for py2.7
        # numA = int(unicode(self.numALoad.text(), "ASCII", "ignore"))
        # numP = int(unicode(self.numPLoad.text(), "ASCII", "ignore"))
        # numI = int(unicode(self.numILoad.text(), "ASCII", "ignore"))
        # numC = int(unicode(self.numCLoad.text(), "ASCII", "ignore"))

        # for py3.4
        numA = int(self.numALoad.text())
        numP = int(self.numPLoad.text())
        numI = int(self.numILoad.text())
        numC = int(self.numCLoad.text())
        print(numA, numP, numI, numC)
        tempStr = "numA:%d numP:%d numI:%d numC:%d" % (numA, numP, numI, numC)
        self.console3.setText(tempStr)
        result = remote_sensingLabel.RSLabel(self.RS_image_file_name, self.RS_label_file_name, numA, numP, numI, numC)

    def OnButton(self):
        for i in range(10):
            if self.radioButtons[i].isChecked():
                print(i)
                self.selectedSample.label = i


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = LabelWindow()
    widget.show()
    app.exec_()

# coding=utf-8
# label windows
import sys
import os
from PyQt4 import QtGui, QtCore
from CaffeProject.util.label_class import GroundTruth
from CaffeProject.util.parameter import Para
class LabelWindow(QtGui.QWidget):
    def __init__(self,  RSRGBImage, cluster_image, sample, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Label')
        self.selectedSample = sample
        optionsGridlayout = QtGui.QGridLayout()
        labelClass = GroundTruth()
        self.radioButtons = []
        for i in range(labelClass.num):
            str = labelClass.GTClass[i]
            tempRadioButton = QtGui.QRadioButton(str)
            self.radioButtons.append(tempRadioButton)
            optionsGridlayout.addWidget(tempRadioButton, i+1, 1)
        self.button = QtGui.QPushButton("Label")
        optionsGridlayout.addWidget(self.button, labelClass.num+1, 1)

        self.connect(self.button,        # 按钮事件
            QtCore.SIGNAL('clicked()'),
            self.OnButton)
        buttonsGridLayout = QtGui.QGridLayout()
        m = len(cluster_image)
        self.buttons = []
        for i in range(m):
            tempButton = QtGui.QToolButton()
            # cluster center image
            tempButton.setIcon(QtGui.QIcon(cluster_image[i]))
            # tempButton.setIcon(QtGui.QIcon("e:\\test.jpg"))
            tempButton.setIconSize(QtCore.QSize(200, 100))
            self.buttons.append(tempButton)
            buttonsGridLayout.addWidget(QtGui.QLabel("cluster%d" % (i+1)), i+1, 1)
            buttonsGridLayout.addWidget(tempButton, i+1, 2)
        widgetLayout = QtGui.QHBoxLayout()
        tempButton = QtGui.QToolButton()
        # remote sensing RGB image
        tempButton.setIcon(QtGui.QIcon(RSRGBImage))
        tempButton.setIconSize(QtCore.QSize(300, 500))
        widgetLayout.addWidget(tempButton, 1)
        widgetLayout.addLayout(buttonsGridLayout, 1)
        widgetLayout.addLayout(optionsGridlayout)
        self.setLayout(widgetLayout)


    def OnButton(self):
        for i in range(10):
            if self.radioButtons[i].isChecked():
                print(i)
                self.selectedSample.label = i


def getLabel():
    app = QtGui.QApplication(sys.argv)
    imagefilename = os.path.join(Para.root, "tmp\\test.jpg")
    widget = LabelWindow(imagefilename, "", None)
    widget.show()
    app.exec_()


if __name__ == "__main__":
    getLabel()
    print("return to main")
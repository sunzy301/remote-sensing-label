# full demo
import sys
from PyQt4 import QtGui, QtCore
class Demo5Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('Label')
        optionsGridlayout = QtGui.QGridLayout()
        n = 10
        self.radioButtons = []
        for i in range(n):
            str = "option%d" % i
            tempRadioButton = QtGui.QRadioButton(str)
            self.radioButtons.append(tempRadioButton)
            optionsGridlayout.addWidget(tempRadioButton, i+1, 1)
        self.button = QtGui.QPushButton("Label")
        optionsGridlayout.addWidget(self.button, n+1, 1)

        self.connect(self.button,        # 按钮事件
            QtCore.SIGNAL('clicked()'),
            self.OnButton)
        buttonsGridLayout = QtGui.QGridLayout()
        m = 5
        self.buttons = []
        for i in range(m):
            tempButton = QtGui.QToolButton()
            tempButton.setIcon(QtGui.QIcon("e:\\test.jpg"))
            tempButton.setIconSize(QtCore.QSize(200, 100))
            self.buttons.append(tempButton)
            buttonsGridLayout.addWidget(QtGui.QLabel("cluster%d" % (i+1)), i+1, 1)
            buttonsGridLayout.addWidget(tempButton, i+1, 2)
        widgetLayout = QtGui.QHBoxLayout()
        tempButton = QtGui.QToolButton()
        tempButton.setIcon(QtGui.QIcon("e:\\kobe.png"))
        tempButton.setIconSize(QtCore.QSize(300, 500))
        widgetLayout.addWidget(tempButton, 1)
        widgetLayout.addLayout(buttonsGridLayout, 1)
        widgetLayout.addLayout(optionsGridlayout)
        self.setLayout(widgetLayout)


    def OnButton(self):
        for i in range(10):
            if self.radioButtons[i].isChecked():
                print(i)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = Demo5Widget()
    widget.show()
    sys.exit(app.exec_())
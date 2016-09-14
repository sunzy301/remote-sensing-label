import sys
from PyQt4 import QtGui, QtCore
# use icon to display image
class Demo3Wdiget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        toolButton1=QtGui.QToolButton()
        toolButton1.setText(self.tr("gavin"))
        toolButton1.setIcon(QtGui.QIcon("e:\\test.jpg"))
        tempIcon = QtGui.QIcon("e:\\test.jpg")
        print(tempIcon)
        toolButton1.setIconSize(QtCore.QSize(200, 200))
        toolButton1.setAutoRaise(True)
        # toolButton1.setToolButtonStyle(QtGui.ToolButtonTextBesideIcon)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(toolButton1)

        self.setLayout(vbox)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = Demo3Wdiget()
    # widget.show()
    sys.exit(app.exec_())
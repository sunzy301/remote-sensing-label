import sys
from PyQt4 import QtGui

# pyqt: GridLayout
class LabelWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Label")
        net_grid = QtGui.QGridLayout()
        for i in range(5):
            net_grid.addWidget(QtGui.QLabel("%d" % i), i, 0)
            net_grid.addWidget(QtGui.QLabel("%d" % (i+1)), i, 1)

        self.setLayout(net_grid)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    qb = LabelWidget()
    qb.show()
    sys.exit(app.exec_())

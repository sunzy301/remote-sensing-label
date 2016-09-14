import sys
from PyQt4 import QtGui

# graphicview
class LabelWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Label")
        self.graphicsView = QtGui.QGraphicsView()
        pixmap = QtGui.QPixmap()
        pixmap.load("e:\\kobe.png")
        self.scene = QtGui.QGraphicsScene(self)
        item = QtGui.QGraphicsPixmapItem(pixmap)
        print(pixmap.height(), pixmap.width())
        self.scene.addItem(item)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    qb = LabelWidget()
    # qb.show()
    sys.exit(app.exec_())

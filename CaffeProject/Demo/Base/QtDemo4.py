# checkbox,radiobox
import sys
from PyQt4 import QtGui, QtCore

class Demo4Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle('PyQt')       # 设置窗口标题
        self.resize(300,200)        # 设置窗口大小
        gridlayout = QtGui.QGridLayout()     # 创建布局组件
        self.label1 = QtGui.QLabel('Label1')    # 创建标签
        self.label2 = QtGui.QLabel('Label2')
        gridlayout.addWidget(self.label1, 1, 2)
        gridlayout.addWidget(self.label2, 2, 2)
        self.radio1 = QtGui.QRadioButton('Radio1')   # 创建单选框
        self.radio2 = QtGui.QRadioButton('Radio2')
        self.radio3 = QtGui.QRadioButton('Radio3')
        self.radio1.setChecked(True)      # 将Radio1选中
        gridlayout.addWidget(self.radio1, 1, 1 )   # 添加单选框
        gridlayout.addWidget(self.radio2, 2, 1 )
        gridlayout.addWidget(self.radio3, 3, 1 )
        self.check = QtGui.QCheckBox('check')    # 创建复选框
        self.check.setChecked(True)       # 将复选框选中
        gridlayout.addWidget(self.check, 3, 2)
        self.button = QtGui.QPushButton('Test')   # 创建按钮
        gridlayout.addWidget(self.button, 4, 1, 1, 2)
        self.setLayout(gridlayout)       # 向窗口中添加布局组件
        self.connect(self.button,        # 按钮事件
            QtCore.SIGNAL('clicked()'),
            self.OnButton)

    def OnButton(self):          # 按钮插槽函数
        if self.radio1.isChecked():       # 判断单选框是否选中
            self.label1.setText('Radio1')
        elif self.radio2.isChecked():
            self.label1.setText('Radio2')
        else:
            self.label1.setText('Radio3')
        if self.check.isChecked():       # 判断复选框是否选中
            self.label2.setText('checked')
        else:
            self.label2.setText('uncheck')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = Demo4Widget()
    widget.show()
    sys.exit(app.exec_())
#coding=utf-8

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()
		self.label = QtGui.QLabel(self)
		self.initUI()
	def initUI(self):
		#self.setGeometry(300, 300, 280, 170)

		# 透明度
		self.setWindowOpacity(1)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		# 去除边框
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		
		self.label.setText('Hello World!')
		self.label.setFont(QtGui.QFont("Microsoft Yahei",50,QtGui.QFont.Bold))
		# 自动调整大小
		self.label.adjustSize()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		# 设置颜色
		pe = QtGui.QPalette() 
		pe.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255,255))#设置字体颜色 
		self.label.setPalette(pe)

		self.adjustSize()
		self.show()
	def paintEvent(self, e):
		qp = QtGui.QPainter()
		qp.begin(self)
		qp.fillRect(self.label.x(),self.label.y()-5,self.label.width(),self.label.height()+10, QtGui.QColor(0,0,0,169))
		qp.end()

app = QtGui.QApplication(sys.argv)
trans = Example()


# trans.setAutoFillBackground(True)
# palette = QtGui.QPalette()
# palette.setColor(QtGui.QPalette.Background, QtGui.QColor(0,253,0,8))
# trans.setPalette(palette)

sys.exit(app.exec_())
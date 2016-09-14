#coding=utf-8

import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()
		self.label = QtGui.QLabel(self)
		self.stackBottom = [0,0]
		self.temp = [0,0]
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

	def keyPressEvent(self, e):
	 	if e.key() == QtCore.Qt.Key_Escape:
			self.close()

	def mousePressEvent(self, e):
		self.temp = [e.x(), e.y()]

	def mouseMoveEvent(self,e):  
		self.setGeometry(self.x()+e.x()-self.temp[0], self.y()+e.y()-self.temp[1], self.width(), self.height())
		self.temp[0]

app = QtGui.QApplication(sys.argv)
trans = Example()

sys.exit(app.exec_())
#coding=utf-8

import sys
from PyQt4 import QtGui, QtCore
import sip

class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()
		self.label = [QtGui.QLabel(self)]
		self.labelNum = 0
		self.temp = [0,0]

		self.initUI()
	def initUI(self):
		#self.setGeometry(300, 300, 280, 170)

		# 透明度
		self.setWindowOpacity(1)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		# 去除边框
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		
		self.label[0].setText('Hello World!')
		self.label[0].setFont(QtGui.QFont("Microsoft Yahei",50,QtGui.QFont.Bold))
		# 自动调整大小
		self.label[0].adjustSize()
		self.label[0].setAlignment(QtCore.Qt.AlignCenter)
		# 设置颜色
		pe = QtGui.QPalette() 
		pe.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255,255))#设置字体颜色 
		self.label[0].setPalette(pe)

		self.labelNum = 1

		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.OnTimer)
		self.timer.start( 2000 )
		self.qp = QtGui.QPainter()
		self.adjustSize()
		self.show()

	def OnTimer(self):
		self.timer.stop()

		temp = len(self.label)-2
		for i in self.label[:0:-1]:
			i.setGeometry(self.label[temp].x(), self.label[temp].y(), i.width(), i.height())
			temp -= 1
		temp = 0
		sip.delete(self.label[0])
		for i in self.label[1:]:
			self.label[temp] = i
			temp += 1

		del self.label[len(self.label)-1]
		print self.label
		self.labelNum -= 1
		if len(self.label) != 0:
			self.timer.start( 2000 )


	def paintEvent(self, e):
		
		self.qp.begin(self)
		tempPosi = [0, 0];
		for i in self.label:
			tempPosi[0] += i.width()
			tempPosi[1] += i.height()
		self.qp.fillRect(0,0,tempPosi[0],tempPosi[1]+10, QtGui.QColor(0,0,0,169))
		# self.qp.fillRect(self.label[0].x(),self.label[0].y()-5,self.label[0].width(),self.label[0].height()+10, QtGui.QColor(0,0,0,169))
		self.qp.end()


	def keyPressEvent(self, e):

	 	if e.key() == QtCore.Qt.Key_Escape:
			self.close()
		else:
			if e.key() == QtCore.Qt.Key_A:
				self.insertMessage("test")


	def mousePressEvent(self, e):
		self.temp = [e.x(), e.y()]

	def mouseMoveEvent(self,e):
		self.setGeometry(self.x()+e.x()-self.temp[0], self.y()+e.y()-self.temp[1], self.width(), self.height())
		self.temp[0]

	def insertMessage(self, str):
		tempLabel = QtGui.QLabel(self)
		tempLabel.setText(str)
		tempLabel.setFont(QtGui.QFont("Microsoft Yahei",50,QtGui.QFont.Bold))
		if self.labelNum != 0:
			tempLabel.setGeometry(self.label[self.labelNum-1].x(), self.label[self.labelNum-1].y()+self.label[self.labelNum-1].height(),self.label[self.labelNum-1].width(),self.label[self.labelNum-1].height())
		else:
			self.timer.start( 2000 )
		# 自动调整大小
		tempLabel.adjustSize()
		tempLabel.setAlignment(QtCore.Qt.AlignCenter)
		# 设置颜色
		pe = QtGui.QPalette() 
		pe.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255,255))#设置字体颜色 
		tempLabel.setPalette(pe)

		tempLabel.show()

		self.labelNum += 1
		self.label += [tempLabel]

		self.adjustSize()

app = QtGui.QApplication(sys.argv)
trans = Example()


sys.exit(app.exec_())
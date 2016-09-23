#coding=utf-8

import sys
import socket
import time
from PyQt4 import QtGui, QtCore

layer = 20
timeP = 1000
delay = 9000
slot = 5000
HOST='133.130.116.215'
PORT=8080

class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()
		self.label = QtGui.QLabel(self)
		# self.labelNum = 0
		# self.temp = [0,0]
		self.Opacity = 1

		# self.initUI("testtesttesttest")
	def initUI(self, s, basePosi):
		self.setGeometry(basePosi[0], basePosi[1], 280, 170)

		# 透明度
		self.setWindowOpacity(1)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		# 去除边框
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.OnTimer)
		self.timer.start( delay )
		self.qp = QtGui.QPainter()
		# self.adjustSize()
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint|QtCore.Qt.Tool)
		# self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		# self.insertMessage("test")
		# tempLabel = QtGui.QLabel(self)
		# str = "你好123456789"
		self.label.setText(s.decode("utf-8"))
		self.label.setFont(QtGui.QFont("Microsoft Yahei",25))
		# if self.labelNum != 0:
		# self.label.setGeometry(self.label.x(), self.label.y()+self.label.height(),self.label.width(),self.label.height())

		# 自动调整大小
		
		self.label.setAlignment(QtCore.Qt.AlignCenter)

		self.label.adjustSize()
		self.adjustSize()
		# 设置颜色
		pe = QtGui.QPalette() 
		pe.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255,255))#设置字体颜色 
		self.label.setPalette(pe)


	def showAll(self):
		self.label.show()
		self.show()

	def OnTimer(self):
		self.timer.stop()
		self.Opacity -= 1.0/layer
		self.setWindowOpacity(self.Opacity)

		if self.Opacity <= 0:
			self.close()
		else:

			self.timer.start( timeP/layer )
		# print self.Opacity
		

		# if len(self.label) != 0:
		# 	temp = len(self.label)-2
		# 	for i in self.label[:0:-1]:
		# 		i.setGeometry(self.label[temp].x(), self.label[temp].y(), i.width(), i.height())
		# 		temp -= 1
		# 	temp = 0
		# 	self.label[0].close()
		# 	for i in self.label[1:]:
		# 		self.label[temp] = i
		# 		temp += 1

		# 	del self.label[len(self.label)-1]
		# 	self.labelNum -= 1
		
		# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# s.connect((HOST,PORT))
		# cmd = 'new data?'
		# s.sendall(cmd)
		# data=s.recv(1024)
		# print data
		# if data != "-1":
		# 	self.insertMessage(data)
		# s.close()

		# self.timer.start( timeP )


	def paintEvent(self, e):

		self.qp.begin(self)
		# tempPosi = [0, 0];
		# for i in self.label:
		# 	tempPosi[0] += i.width()
		# 	tempPosi[1] += i.height()
		# print self.height()
		# print self.width()
		# print self.label.width()
		self.qp.fillRect(self.label.x(),self.label.y(),self.width(),self.height(), QtGui.QColor(0,0,0,169))
		# self.qp.fillRect(self.label[0].x(),self.label[0].y()-5,self.label[0].width(),self.label[0].height()+10, QtGui.QColor(0,0,0,169))
		self.qp.end()

	# def move(self):
	# 	self.move(10,10)
	# def keyPressEvent(self, e):

	# 	if e.key() == QtCore.Qt.Key_Escape:
	# 		self.close()
	# 	else:
	# 		if e.key() == QtCore.Qt.Key_A:
	# 			self.insertMessage("test")


	def mousePressEvent(self, e):
		self.temp = [e.x(), e.y()]

	def mouseMoveEvent(self,e):
		MeList.base[0] += e.x()-self.temp[0]
		MeList.base[1] += e.y()-self.temp[1]
		if len(MeList.Mlist) != 0:
			for i in MeList.Mlist:
				i.setGeometry(i.x()+e.x()-self.temp[0], i.y()+e.y()-self.temp[1], i.width(), i.height())
				# self.temp[0]

	# def insertMessage(self, str):
	# 	# tempLabel = QtGui.QLabel(self)
	# 	# tempLabel.setText(str.decode("utf-8"))
	# 	# tempLabel.setFont(QtGui.QFont("Microsoft Yahei",25))
	# 	# # if self.labelNum != 0:
	# 	# # 	tempLabel.setGeometry(self.label[self.labelNum-1].x(), self.label[self.labelNum-1].y()+self.label[self.labelNum-1].height(),self.label[self.labelNum-1].width(),self.label[self.labelNum-1].height())

	# 	# # 自动调整大小
	# 	# tempLabel.adjustSize()
	# 	# tempLabel.setAlignment(QtCore.Qt.AlignCenter)
	# 	# # 设置颜色
	# 	# pe = QtGui.QPalette() 
	# 	# pe.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255,255))#设置字体颜色 
	# 	# tempLabel.setPalette(pe)

	# 	# tempLabel.show()

	# 	# self.labelNum += 1
	# 	# self.label += [tempLabel]

	# 	self.adjustSize()


class ExampleList:
	def __init__(self):
		self.Mlist = []
		self.base = [1000, 1000]
		self.MNum = 0
		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.OnTimer)
		self.timer.start( slot )

	def insertMessage(self, s):
		tempM = Example()
		tempM.initUI(s, self.base)
		if len(self.Mlist) != 0:
			for i in self.Mlist:
				i.move(i.x(),i.y()-tempM.height())
		tempM.showAll()
		self.Mlist += [tempM]

	def OnTimer(self):
		# print 1
		# self.insertMessage(str(time.clock()))
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		cmd = 'new data?'
		s.sendall(cmd)
		data=s.recv(1024)
		# print data
		if data != "-1":
			self.insertMessage(data)
		s.close()



def appQuit():
	print "OK!"
	app.quit()
	


app = QtGui.QApplication(sys.argv)

 
icon = QtGui.QIcon("icon.ico")
trayIcon = QtGui.QSystemTrayIcon(app)
trayIcon.setIcon(icon)
trayIcon.setToolTip("Blive")
trayIcon.show()
trayIcon.activated.connect(appQuit)

# trans = Example()

# trans.initUI("testtesttesttest")
# trans.showAll()

MeList = ExampleList()

sys.exit(app.exec_())

